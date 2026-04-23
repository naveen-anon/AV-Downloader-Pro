import os, sys, shutil, json, urllib.request, zipfile, platform from pathlib import Path from colorama import init, Fore, Style from yt_dlp import YoutubeDL

init(autoreset=True) VERSION='2.0.0' DEV='naveen_anon' REPO_API='https://api.github.com/repos/yourusername/AV-Downloader-Pro/releases/latest' HOME=Path.home() TERMUX='com.termux' in str(HOME) or os.getenv('PREFIX','').startswith('/data/data/com.termux') SAVE_DIR=(HOME/'storage'/'downloads') if TERMUX else (HOME/'Videos') SAVE_DIR.mkdir(parents=True, exist_ok=True)

BANNER=f'''{Fore.RED} █████╗ ██╗   ██╗ ██╔══██╗██║   ██║ ███████║██║   ██║ ██╔══██║╚██╗ ██╔╝ ██║  ██║ ╚████╔╝ ╚═╝  ╚═╝  ╚═══╝ {Fore.YELLOW}AV Downloader Pro {VERSION} {Fore.CYAN}YouTube • Shorts • MP3 {Fore.GREEN}Termux • Kali • NetHunter {Fore.MAGENTA}Developer: {DEV} {Fore.WHITE}Save Folder: {SAVE_DIR} '''

def clear(): os.system('clear' if os.name!='nt' else 'cls') def ffmpeg_ok(): return shutil.which('ffmpeg') is not None

def check_update(): try: with urllib.request.urlopen(REPO_API, timeout=4) as r: data=json.loads(r.read().decode()) latest=data.get('tag_name','').replace('v','') if latest and latest!=VERSION: print(Fore.YELLOW+f'[UPDATE] New version available: {latest}') except: pass

def download(url, mode, quality='best'): post=[]; fmt='best' if mode=='1': fmt='bestvideo+bestaudio/best' if quality=='best' else f'bestvideo[height<={quality}]+bestaudio/best' elif mode=='2': fmt='best[height<=1080]/best' elif mode=='3': fmt='bestaudio/best' post=[{'key':'FFmpegExtractAudio','preferredcodec':'mp3','preferredquality':'192'}] opts={ 'outtmpl': str(SAVE_DIR/'%(title)s.%(ext)s'), 'format': fmt, 'merge_output_format':'mp4', 'postprocessors': post, 'noplaylist': True } with YoutubeDL(opts) as y: y.download([url])

def make_zip(): z='AV_Downloader_Pro_Portable.zip' with zipfile.ZipFile(z,'w') as f: f.write(file, arcname='av_downloader_pro_all_in_one.py') print(Fore.GREEN+f'Created {z}')

while True: clear(); print(BANNER); check_update() if not ffmpeg_ok(): print(Fore.RED+'[!] ffmpeg not installed (recommended)\n') print(Fore.YELLOW+'[1] Download Video') print(Fore.CYAN+'[2] Download Shorts') print(Fore.GREEN+'[3] Download MP3') print(Fore.BLUE+'[4] Create ZIP Release') print(Fore.MAGENTA+'[5] Open Save Folder') print(Fore.RED+'[6] Exit\n') ch=input('Choose: ').strip() if ch=='6': sys.exit() elif ch=='5': print(SAVE_DIR); input('Enter...') elif ch=='4': make_zip(); input('Enter...') elif ch in ('1','2','3'): url=input('URL: ').strip(); q='best' if ch=='1': q=input('360/480/720/1080/best: ').strip() or 'best' try: download(url,ch,q) print(Fore.GREEN+'Done!') except Exception as e: print(Fore.RED+str(e)) input('Enter...')
