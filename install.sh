#!/bin/bash
clear
echo "Installing AV Downloader Pro..."
if command -v pkg >/dev/null 2>&1; then
    pkg update -y
    pkg install python ffmpeg -y
    pip install -r requirements.txt
    termux-setup-storage
else
    sudo apt update
    sudo apt install python3-pip ffmpeg -y
    pip3 install -r requirements.txt
fi
echo "Install Complete"
