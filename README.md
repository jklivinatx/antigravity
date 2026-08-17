# Antigravity Workspace

A central, consolidated repository for Antigravity agent skills, workflows, automation scripts, job queries, and tools.

---

## 📁 Repository Structure

```text
gravity/
├── .agents/
│   ├── skills/
│   │   └── youtube-mp3-downloader/     # Reusable skill for downloading & converting YouTube audio
│   └── workflows/
│       └── download-playlist.md        # Step-by-step workflow for YouTube playlists
├── YT-DLP/                             # YouTube download & chapter splitting scripts and guides
│   ├── Downloading playlists to mp3 on iphone.md
│   ├── download_playlist.py / .bat
│   └── split_chapters.py / .bat
├── job-query/                          # Job search & scraper scripts
│   ├── fetch_nyrr_jobs.py
│   └── nyrr_job_openings.md
├── bind-windscribe/                    # Network & VPN background documentation
│   └── background.md
├── scripts/                            # Utility scripts & command references
│   ├── downloadplaylist.py
│   ├── extract_and_cleanup.bat
│   └── git commands.txt
├── Workspaces/                         # Antigravity & VS Code workspace configs
└── README.md
```

---

## 🚀 Key Workflows & Tools

### 1. YouTube to MP3 Downloader
- **Skill:** [youtube-mp3-downloader](.agents/skills/youtube-mp3-downloader/SKILL.md)
- Automatically downloads audio from YouTube videos or playlists and converts them to high-quality MP3s saved directly to your `Downloads` folder.

### 2. Job Query Scrapers
- **Script:** [`fetch_nyrr_jobs.py`](job-query/fetch_nyrr_jobs.py)
- Fetches and formats job openings from NYRR into markdown documentation.

### 3. Audio & Chapter Tools
- Scripts in [`YT-DLP/`](YT-DLP/) provide utilities for splitting audio files by chapter markers and batch downloading playlists.

---

## ⚙️ Requirements
- Python 3.10+
- `yt-dlp` (`pip install yt-dlp`)
- `ffmpeg` (for media encoding and conversion)
