import os
import re
import shlex
import subprocess
import yt_dlp
import glob

def sanitize_title(title):
    # Replace problematic characters with an underscore or remove them
    sanitized_title = re.sub(r'[\\/*?:"<>|]', '_', title)  # Replaces invalid characters
    sanitized_title = re.sub(r'[^\w\s-]', '', sanitized_title)  # Removes non-ASCII characters
    return sanitized_title.strip()

def download_and_convert(url):
    # Step 1: Get the video title using yt-dlp
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'force_generic_extractor': False
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        title = info_dict.get('title', None)

    if title is None:
        print("Error: Unable to retrieve video title.")
        return

    # Sanitize the title for file usage
    sanitized_title = sanitize_title(title)
    print(f"Sanitized title: {sanitized_title}")

    # Step 2: Download the video using yt-dlp with sanitized title as filename
    video_filename = f"{sanitized_title}.%(ext)s"
    print(f"Downloading video as {video_filename}...")
    download_opts = {
        'outtmpl': video_filename
    }
    with yt_dlp.YoutubeDL(download_opts) as ydl:
        ydl.download([url])

    # Step 3: Find the downloaded file (in case it's not mp4)
    downloaded_files = glob.glob(f"{sanitized_title}.*")
    if not downloaded_files:
        print(f"Error: Could not find the downloaded video file for {sanitized_title}")
        return
    input_file = downloaded_files[0]  # First matching file
    print(f"Downloaded file: {input_file}")

    # Step 4: Set the output file path to the ~/Music directory
    music_directory = os.path.expanduser("~/Music")
    if not os.path.exists(music_directory):
        os.makedirs(music_directory)
    output_file = os.path.join(music_directory, f"{sanitized_title}.mp3")

    print(f"Converting {input_file} to MP3 as {output_file}...")

    # Use shlex.quote to handle filenames with spaces or special characters
    ffmpeg_command = f'ffmpeg -i {shlex.quote(input_file)} -q:a 0 -map a {shlex.quote(output_file)}'

    try:
        subprocess.run(ffmpeg_command, shell=True, check=True)
        print(f"Conversion complete. The MP3 file is saved as '{output_file}'.")
    except subprocess.CalledProcessError:
        print("Error: Failed to convert video to MP3.")
        return

    # Optional: Clean up the downloaded video file after conversion
    os.remove(input_file)

if __name__ == "__main__":
    video_url = input("Enter the video URL: ")
    download_and_convert(video_url)
