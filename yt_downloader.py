import os
import sys
import shutil
import platform
from pathlib import Path
from colorama import init, Fore
from yt_dlp import YoutubeDL

init(autoreset=True)

HOME = Path.home()

# Detect environment
TERMUX = "com.termux" in str(HOME) or os.getenv("PREFIX", "").startswith("/data/data/com.termux")
NETHUNTER = "kali" in platform.platform().lower()

# Save path
if TERMUX:
    SAVE_DIR = HOME / "storage" / "downloads"
else:
    SAVE_DIR = HOME / "Videos"

SAVE_DIR.mkdir(parents=True, exist_ok=True)

# Banner
BANNER = f"""
{Fore.RED}███╗   ██╗ {Fore.YELLOW}AV Downloader Pro
{Fore.GREEN}████╗  ██║ {Fore.CYAN}YouTube / Shorts / Audio
{Fore.BLUE}██╔██╗ ██║ {Fore.MAGENTA}Termux + Kali + NetHunter
{Fore.WHITE}Developer: naveen_anon
{Fore.YELLOW}Save Folder: {SAVE_DIR}
"""

def clear():
    os.system("clear" if os.name != "nt" else "cls")

def ffmpeg_ok():
    return shutil.which("ffmpeg") is not None

def download(url, mode, quality="best"):
    post = []
    fmt = "best"

    if mode == "1":  # Video
        if quality == "best":
            fmt = "bestvideo+bestaudio/best"
        else:
            fmt = f"bestvideo[height<={quality}]+bestaudio/best"

    elif mode == "2":  # Shorts
        fmt = "best[height<=1080]/best"

    elif mode == "3":  # MP3
        fmt = "bestaudio/best"
        post = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192"
        }]

    opts = {
        "outtmpl": str(SAVE_DIR / "%(title)s.%(ext)s"),
        "format": fmt,
        "merge_output_format": "mp4",
        "noplaylist": True,
        "postprocessors": post,
        "quiet": False
    }

    with YoutubeDL(opts) as ydl:
        ydl.download([url])

def menu():
    print(Fore.YELLOW + "[1] Download Video")
    print(Fore.CYAN + "[2] Download Shorts")
    print(Fore.GREEN + "[3] Download Audio MP3")
    print(Fore.MAGENTA + "[4] Open Save Folder")
    print(Fore.RED + "[5] Exit\n")

while True:
    clear()
    print(BANNER)

    if not ffmpeg_ok():
        print(Fore.RED + "[!] ffmpeg not installed (recommended)\n")

    menu()
    choice = input("Choose option: ").strip()

    if choice == "5":
        sys.exit()

    elif choice == "4":
        print(f"\nSaved files location:\n{SAVE_DIR}")
        input("\nPress Enter...")
        continue

    elif choice in ["1", "2", "3"]:
        url = input("Enter YouTube URL: ").strip()
        quality = "best"

        if choice == "1":
            quality = input("Quality 360/480/720/1080 or best: ").strip() or "best"

        try:
            download(url, choice, quality)
            print(Fore.GREEN + f"\nDownload completed!\nSaved in: {SAVE_DIR}")
        except Exception as e:
            print(Fore.RED + f"\nError: {e}")

        input("\nPress Enter to continue...")

    else:
        input("Invalid option! Press Enter...")
