import subprocess
import os

def main():
    print("==================================================")
    print("      YouTube Playlist to MP3 Downloader (iOS)")
    print("==================================================")
    
    url = input("\nPlease enter the YouTube Playlist or Video URL: ").strip()
    
    if not url:
        print("No URL provided. Exiting.")
        return

    print(f"\nDownloading and converting: {url}")
    
    # This command matches your Windows settings exactly
    command = [
        "yt-dlp",
        "-x",
        "--audio-format", "mp3",
        "--audio-quality", "0",
        "-o", "%(playlist_title)s/%(playlist_index)02d - %(title)s.%(ext)s",
        url
    ]
    
    try:
        # Run yt-dlp through the shell
        subprocess.run(command, check=True)
        print("\nDone! Your files are ready in your a-Shell folder.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Make sure you have run 'pip install yt-dlp' first.")

if __name__ == "__main__":
    main()
