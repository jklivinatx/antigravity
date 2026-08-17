@echo off
setlocal

echo ==================================================
echo       YouTube Chapter Splitter (MP3)
echo ==================================================
echo.

:: Check if a URL was dragged-and-dropped onto the file (%1)
set "URL=%~1"

if "%URL%"=="" (
    echo Please enter the YouTube Video URL:
    set /p URL=
)

if "%URL%"=="" (
    echo.
    echo No URL provided. Exiting.
    pause
    exit /b
)

echo.
echo Processing chapters...
echo This may take a few minutes depending on video length.
echo URL: %URL%

:: Run yt-dlp
:: -x: Extract audio
:: --audio-format mp3: Convert to MP3
:: --audio-quality 0: Best quality (VBR)
:: --split-chapters: Split by chapters
:: -o "chapter:...": Template for the split files (Folder/ChapterName.mp3)
:: -o "...": Template for the main file (Folder/FullVideo.mp3)
".\yt-dlp.exe" -x --audio-format mp3 --audio-quality 0 --split-chapters -o "chapter:%%(title)s/%%(section_title)s.%%(ext)s" -o "%%(title)s/%%(title)s [FULL].%%(ext)s" "%URL%"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Done! Your files are ready in the folder named after the video.
) else (
    echo.
    echo Something went wrong. Make sure yt-dlp.exe and ffmpeg.exe are in this folder.
)

pause

