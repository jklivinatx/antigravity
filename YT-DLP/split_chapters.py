import subprocess
import os
import sys

def main():
    """
    Downloads a YouTube video, extracts high-quality MP3 audio, 
    and splits it into separate files based on chapters.
    """
    print("==================================================")
    print("      YouTube Chapter Splitter (MP3)")
    print("==================================================")
    
    # Check if URL was passed as an argument (like drag-and-drop or CLI)
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("\nPlease enter the YouTube Video URL: ").strip()
    
    if not url:
        print("No URL provided. Exiting.")
        return

    print(f"\nProcessing: {url}")
    print("Phase 1: Downloading & Converting to MP3")
    print("Phase 2: Splitting by Chapters")
    print("-" * 50)

    # Use local exe if available, otherwise assume it's in the system PATH
    yt_dlp_exe = "./yt-dlp.exe" if os.path.exists("./yt-dlp.exe") else "yt-dlp"

    # Construct the command
    # Note: No need for double percents (%%) in Python strings
    command = [
        yt_dlp_exe,
        "-x",
        "--audio-format", "mp3",
        "--audio-quality", "0",
        "--split-chapters",
        "-o", "chapter:%(title)s/%(section_title)s.%(ext)s",
        "-o", "%(title)s/%(title)s [FULL].%(ext)s",
        url
    ]
    
    try:
        # Execute the command
        subprocess.run(command, check=True)
        print("\n" + "=" * 50)
        print("SUCCESS: Your files are ready in the folder named after the video.")
        print("=" * 50)
    except subprocess.CalledProcessError:
        print("\nERROR: yt-dlp failed. Check the URL or your internet connection.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        print("Ensure yt-dlp.exe and ffmpeg.exe are in this folder.")

    # Keep window open if run via double-click on Windows
    input("\nPress Enter to close...")

if __name__ == "__main__":
    main()
