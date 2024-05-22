import os
import sys
import urllib.request
import json
import os, sys; sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
from username import username

import pygame

import os, sys; sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
from username import username

def play_wav_file(file_path):
    
    # pygame 초기화
    pygame.init()
    try:
        # WAV 파일 로드
        sound = pygame.mixer.Sound(file_path)
        # 사운드 재생
        sound.play()
        # 재생이 완료될 때까지 대기
        while pygame.mixer.get_busy():
            pygame.time.delay(100)

    except pygame.error as e:
        print("오류 발생:", e)

    finally:
        # pygame 종료
        pygame.quit()





def PrintComment(text):
    
    with open(f"/home/{username}/yykc/tts/api_key.json", 'r') as file:
        config = json.load(file)

    path = f'/home/{username}/yykc/tts/comment/recent_comment.wav'
    client_id = config["client_id"]
    client_secret = config["client_secret"]
    encText = urllib.parse.quote(text)
    data = "speaker=ndain&volume=0&speed=0&pitch=0&format=mp3&text=" + encText
    url = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"
    request = urllib.request.Request(url)
    request.add_header("X-NCP-APIGW-API-KEY-ID",client_id)
    request.add_header("X-NCP-APIGW-API-KEY",client_secret)
    response = urllib.request.urlopen(request, data=data.encode('utf-8'))
    rescode = response.getcode()


    if(rescode==200):
        response_body = response.read()
        with open(path, 'wb') as f:
            f.write(response_body)
    else:
        print("Error Code:" + rescode)

    play_wav_file(path)




