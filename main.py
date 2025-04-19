from typing import Tuple
from plyer import notification
from spotipy.oauth2 import SpotifyOAuth
import argparse
import datetime
import dotenv
import os
import questionary
import spotipy
import time

dotenv.load_dotenv()

# Spotify API credentials - Set these in your environment variables
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI', 'http://localhost')

def select_device_interactively(sp) -> Tuple[str, str]:
    """Let user select a device interactively using arrow keys"""
    devices = sp.devices()
    
    if not devices['devices']:
        raise Exception("No active Spotify device found")
    
    # Create list of device names for the selection
    device_choices = [
        f"{device['name']} ({device['type']})" 
        for device in devices['devices']
    ]
    
    # Add a cancel option
    device_choices.append("Cancel")
    
    selected = questionary.select(
        "Select a device to play on:",
        choices=device_choices
    ).ask()
    
    if selected == "Cancel":
        print("Device selection cancelled")
        exit()
    
    # Find the selected device
    selected_index = device_choices.index(selected)
    device_id = devices['devices'][selected_index]['id']
    
    return selected, device_id

def spotify_alarm(playlist_uri: str, alarm_time: str, volume: int=80) -> None:
    """
    Plays a Spotify playlist at a specified time, with a gradual volume increase.
    Args:
        playlist_uri (str): Spotify playlist URI (e.g., "spotify:playlist:XXX").
        alarm_time (str): Time in "HH:MM" 24-hour format.
        volume (int): Target volume (0-100). Default: 80.
    """
    # Authenticate with Spotify using OAuth
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope="user-read-playback-state,user-modify-playback-state",  # Required permissions
        cache_path=".spotify_cache"  # Stores auth tokens for future runs
    ))

    # Let the user select a device interactively
    selected_device, device_id = select_device_interactively(sp)

    # Normalize alarm_time to ensure leading zeros (e.g., "8:23" → "08:23")
    alarm_time_formatted = datetime.datetime.strptime(alarm_time, "%H:%M").strftime("%H:%M")
    print(f"Alarm set for {alarm_time_formatted} on device {selected_device}. Keep this app running...")
    
    # Main alarm loop
    while True:
        current_time = datetime.datetime.now().strftime("%H:%M")  # Get current time

        # URI for a silent playlist (to minimize pre-alarm noise)
        silence_context_uri = "https://open.spotify.com/playlist/4JZXHm8EZqC8Nq4hD28WRu?si=XXX"

        # Play silent playlist at minimal volume (1%)
        sp.start_playback(device_id=device_id, context_uri=silence_context_uri)
        sp.volume(1, device_id)  # Set volume to 1%

        # Check if it's time to trigger the alarm
        if current_time == alarm_time_formatted:
            # Start playing the target playlist
            sp.start_playback(device_id=device_id, context_uri=playlist_uri)

            # Gradual volume increase (avoids sudden loud noise)
            target_volume = 1  # Start from 1%
            while target_volume < volume:
                target_volume += 5  # Increase by 5% each step
                target_volume = min(target_volume, 100)  # Cap at 100%
                sp.volume(target_volume, device_id)
                time.sleep(0.5)  # Small delay between volume steps
            
            # Send a desktop notification
            notification.notify(
                title="Spotify Alarm",
                message=f"Playing your playlist at {alarm_time}",
                timeout=10  # Notification disappears after 10s
            )
            break  # Exit the loop after triggering
        
        time.sleep(30)  # Check time every 30 seconds

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Spotify Alarm Clock')
    parser.add_argument('--playlist', type=str, required=True,
                       help='Spotify playlist URI (e.g., "spotify:playlist:37i9dQZF1EJW5QYMSm7Z0Q")')
    parser.add_argument('--time', type=str, required=True,
                       help='Alarm time in "HH:MM" format (24-hour)')
    parser.add_argument('--volume', type=int, default=50,
                       help='Initial volume (0-100), default is 50')
    
    args = parser.parse_args()
    
    try:
        datetime.datetime.strptime(args.time, "%H:%M")
    except ValueError:
        raise ValueError("Incorrect time format, should be HH:MM")
    
    spotify_alarm(args.playlist, args.time, args.volume)
