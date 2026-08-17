@echo off
setlocal

echo ==================================================
echo       YouTube Playlist to MP3 Downloader
echo ==================================================
echo.

:: Check if a URL was dragged-and-dropped onto the file (%1)
set "URL=%~1"

if "%URL%"=="" (
    echo Please enter the YouTube Playlist or Video URL:
    set /p URL=
)

if "%URL%"=="" (
    echo.
    echo No URL provided. Exiting.
    pause
    exit /b
)

echo.
echo Downloading and converting...
echo URL: %URL%

:: Run yt-dlp
".\yt-dlp.exe" -x --audio-format mp3 --audio-quality 0 -o "%%(playlist_title)s/%%(playlist_index)02d - %%(title)s.%%(ext)s" "%URL%"

echo.
echo Done! Your files are ready.
pause
