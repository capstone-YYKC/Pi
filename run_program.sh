#!/bin/sh
sudo rdate -s time.bora.net

username=$USER

# 가상 환경 활성화
. /home/$username/venv/bin/activate

# 파이썬 스크립트 실행
python3 /home/$username/yykc/main.py