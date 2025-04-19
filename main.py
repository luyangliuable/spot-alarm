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

def select_device_interactively(sp):
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
    
    return device_id

def spotify_alarm(playlist_uri, alarm_time, volume=50):
    """
    Play a Spotify playlist at a specific time
    
    :param playlist_uri: Spotify playlist URI (e.g., "spotify:playlist:37i9dQZF1EJW5QYMSm7Z0Q")
    :param alarm_time: Time in format "HH:MM" (24-hour)
    :param volume: Initial volume (0-100)
    """
    # Authenticate with Spotify
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope="user-read-playback-state,user-modify-playback-state",
        cache_path=".spotify_cache"
    ))

    # Get current device (must have Spotify client active)
    device_id = select_device_interactively(sp)

    print(f"Alarm set for {alarm_time} on device {device_id}. Keep this app running...")
    
    while True:
        current_time = datetime.datetime.now().strftime("%H:%M")
        print(current_time, alarm_time)

        silence_context_uri="https://open.spotify.com/playlist/4JZXHm8EZqC8Nq4hD28WRu?si=487697d5970e41fd"

        sp.start_playback(
            device_id=device_id,
            context_uri=silence_context_uri
        )

        sp.volume(1, device_id)

        if current_time == alarm_time:
            sp.start_playback(
                device_id=device_id,
                context_uri=playlist_uri
            )

            sp.volume(volume, device_id)
            
            # Send desktop notification
            notification.notify(
                title="Spotify Alarm",
                message=f"Playing your playlist at {alarm_time}",
                timeout=10
            )

            break
        
        time.sleep(30)

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
