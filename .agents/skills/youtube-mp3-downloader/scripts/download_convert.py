import sys
import subprocess
import os

def download_and_convert(url, output_dir=r"C:\Users\cary\Downloads"):
    os.makedirs(output_dir, exist_ok=True)
    print(f"Downloading {url} to {output_dir}...")
    
    # Step 1: Download using Python yt_dlp module
    download_cmd = [
        sys.executable, "-m", "yt_dlp",
        "-f", "bestaudio/best",
        "-o", os.path.join(output_dir, "%(title)s [%(id)s].%(ext)s"),
        url
    ]
    subprocess.run(download_cmd, check=True)
    
    print("Download complete. Starting MP3 conversion...")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        download_and_convert(sys.argv[1])
    else:
        print("Usage: python download_convert.py <YOUTUBE_URL>")
