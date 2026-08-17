---
description: Download a YouTube playlist or video as MP3s
---

# YouTube MP3 Downloader Workflow

This workflow automatically uses `yt-dlp` and `ffmpeg` to download the best quality MP3 audio from a YouTube video or playlist URL.

1. Verify that the necessary executable files exist in the current working directory. The tools are:
   - `yt-dlp.exe`
   - `ffmpeg.exe`
   - `ffprobe.exe`
2. If any of the required tools are missing, automatically download and extract them:
   // turbo
3. Run the following setup command in PowerShell:

   ```powershell
   Invoke-WebRequest -Uri "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe" -OutFile "yt-dlp.exe"; Invoke-WebRequest -Uri "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip" -OutFile "ffmpeg.zip"; Expand-Archive -Path "ffmpeg.zip" -DestinationPath "." -Force; $ffmpegDir = Get-ChildItem -Directory -Filter "ffmpeg-*-essentials_build" | Select-Object -ExpandProperty Name; Move-Item -Path "$ffmpegDir\bin\ffmpeg.exe" -Destination "." -Force; Move-Item -Path "$ffmpegDir\bin\ffprobe.exe" -Destination "." -Force; Remove-Item -Path "ffmpeg.zip" -Force; Remove-Item -Path "$ffmpegDir" -Recurse -Force
   ```

4. Prompt the user for a YouTube URL if they haven't provided one already.
5. Execute the `yt-dlp` download command, ensuring all generated files are structured beautifully using this Output template constraint. We use `--cookies-from-browser firefox` and `--js-runtimes node` to bypass bot checks, and `-U` to update `yt-dlp` first:
   ```powershell
   .\yt-dlp.exe -U; .\yt-dlp.exe -x --audio-format mp3 --audio-quality 0 -o "%(playlist_title)s/%(playlist_index)02d - %(title)s.%(ext)s" --cookies-from-browser firefox --js-runtimes node "<THE YOUTUBE URL>"
   ```
