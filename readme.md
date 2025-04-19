# Spotify Alarm Clock 🎵⏰

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- [Spotify Alarm Clock 🎵⏰](#spotify-alarm-clock-🎵)
    - [Features ✨](#features-✨)
    - [Prerequisites 📋](#prerequisites-📋)
    - [Installation ⚙️](#installation-⚙️)
    - [Usage 🚀](#usage-🚀)
    - [How It Works 🔧](#how-it-works-🔧)
    - [Notes 📝](#notes-📝)

<!-- markdown-toc end -->


A Python script that plays your Spotify playlist at a specified time, functioning as a musical alarm clock. Includes interactive device selection and volume control.

## Features ✨

- 🎶 Play any Spotify playlist at your desired time
- 🖥️ Interactive device selection (computer, phone, web player, etc.)
- 🔉 Volume control (set initial playback volume)
- 🔕 Plays silent audio before alarm time to avoid sudden loud playback
- 🔔 Desktop notification when alarm triggers

## Prerequisites 📋

- Python 3.6+
- Spotify Premium account
- Spotify app running on at least one device

## Installation ⚙️

1. Clone this repository:

```bash
git clone https://github.com/yourusername/spotify-alarm.git
cd spotify-alarm
```

2. Install dependencies:

```
pip install -r requirements.txt
```

3. Set up Spotify Developer credentials:

* Go to Spotify Develope rDashboard
* Create a new app
* Add http://localhost as a Redirect URI

4. Create a .env file with your credentials:

```
SPOTIPY_CLIENT_ID=your_client_id
SPOTIPY_CLIENT_SECRET=your_client_secret
```

## Usage 🚀

Basic command:

```
python3 main.py \
  --playlist "PLAYLIST_URL" \
  --time 22:18 \
  --volume 100
```

Arguments:

* `--playlist`: Spotify playlist URL or URI (required)
* `--time`: Alarm time in 24-hour format (HH:MM) (required)
* `--volume`: Initial volume (0-100, default: 50)

Example:

```bash
python3 main.py \
  --playlist "spotify:playlist:37i9dQZF1EJW5QYMSm7Z0Q" \
  --time 07:30 \
  --volume 75
```

## How It Works 🔧
* The script authenticates with Spotify using OAuth
* Presents an interactive menu to select playback device
* Continuously checks current time vs alarm time
* Before alarm time, plays silent audio at minimum volume
* At exact alarm time, switches to your playlist at specified volume
* Shows desktop notification when alarm triggers

## Notes 📝
* Keep the script running until alarm triggers
* Make sure your selected device is active and online
* First run will open browser for Spotify authentication
* Subsequent runs will use cached credentials
