# YouTube Mp3 for Linux

This script allows you to download music from YouTube/YTMusic by copying the share link and convert it to MP3 format.

## Requirements

- `Python 3.12+`
- `python3-venv`
- `yt-dlp`
- `ffmpeg`

## Installation

**Clone the repository:**

```bash
git clone https://github.com/riefqikml/ytmp3.git
cd ytmp3
```

**Set Up a Virtual Environment and Install Dependencies**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

**Run the Script**

```bash
python3 main.py
```

**Enter the YouTube Video URL**

When prompted, paste the YouTube video URL you want to download. The mp3 will automatically saved at ~/Music directory.
