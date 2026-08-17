---
name: youtube-mp3-downloader
description: >-
  Use this skill when the user asks to download a YouTube video or convert a YouTube video/audio link to an MP3 file saved to their Downloads folder.
---

# YouTube MP3 Downloader & Converter Skill

This skill provides automated instructions for downloading YouTube media and converting audio to MP3 format.

## Steps

1. **Target Directory:** Downloads and converted files are saved directly to `C:\Users\cary\Downloads\`.
2. **Download Execution:** Execute `python -m yt_dlp` or run the helper script:
   `python .agents/skills/youtube-mp3-downloader/scripts/download_convert.py "<URL>"`
3. **Audio Conversion:** Use `ffmpeg` to extract high-quality MP3 audio:
   `ffmpeg -vn -i "<INPUT_FILE>" -acodec libmp3lame -q:a 2 "<OUTPUT_MP3>"`
4. **Long-Running Tasks:** Run long audio conversions asynchronously in background tasks and notify the user when finished.
