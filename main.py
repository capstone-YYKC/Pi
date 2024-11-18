import bert.predict_emotion
import switch
from ai_api.create_comment import CreateComment
from stt.stt import SpeechToText
from tts.tts import PrintComment
from tts.tts import play_wav_file
import requests
import threading

import time

import motor.mttest2

from username import username



stop_event = threading.Event()

emotion, result_emotion, result_count = None, None, None


def motor_threading(content, stop_event):
    global emotion, result_emotion, result_count

    emotion = bert.predict_emotion.predict(content)      # 감정 예측값
    emotion_counts_excluding_neutral = {key: value for key, value in emotion.items() if key != "보통"}
    max_other_emotion = max(emotion_counts_excluding_neutral, key=emotion_counts_excluding_neutral.get)
    max_other_count = emotion_counts_excluding_neutral[max_other_emotion]
    result_emotion, result_count = ("보통", emotion["보통"]) if max_other_count == 0 else (max_other_emotion, max_other_count)
   
    if result_emotion == "행복":
        motor.mttest2.waving_hand(stop_event)
    elif result_emotion == "슬픔":
        motor.mttest2.hug(stop_event)
    else:
        motor.mttest2.nodding(stop_event)

    

def process():
    global stop_event
    global emotion, result_emotion, result_count

    # 1. STT
    # SppechToText : 마이크 입력을 text로 리턴
    content = SpeechToText()
    print(f"사용자 입력: {content}")


    # 3. 코멘트 생성 및 출력
    #CreateComment: 다이어리를 인풋으로 넣으면 comment를 리턴
    comment = CreateComment(content) # 사용자에게 출력할 코멘트
    print(f"comment: {comment}")

    # 모터 제어 스레드
    motor_thread = threading.Thread(target = motor_threading, args=(content,stop_event))
    stop_event.clear()
    motor_thread.start()

    PrintComment(comment)

    # 코멘트 출력이 끝나면 모터제어도 종료.
    stop_event.set()
    motor_thread.join() 


    # 4. 감정 예측
    # predict : 
    # 감정 예측값 리턴
    # emotion = bert.predict_emotion.predict(content)      # 감정 예측값

    # 보통을 제외한 최댓값 구하기.
    # emotion_counts_excluding_neutral = {key: value for key, value in emotion.items() if key != "보통"}
    # max_other_emotion = max(emotion_counts_excluding_neutral, key=emotion_counts_excluding_neutral.get)
    # max_other_count = emotion_counts_excluding_neutral[max_other_emotion]
    # result_emotion, result_count = ("보통", emotion["보통"]) if max_other_count == 0 else (max_other_emotion, max_other_count)

    emotion_score = round(bert.predict_emotion.calculate_emotion_score(emotion),2)

    # 5. 서버로 전송
    url  = 'https://www.gomgom.shop/diary'

    # # transcribe_streaming_mic redirection data
    # # diary content 

    data = {
        'userId' : 1,                  # 유저구분
        'emotionStatus' : result_emotion,        # 감정
        'emotionScore' : emotion_score,          # 감정점수
        'content': content              # 일기
        # 'consolation': comment       # 생성된 코멘트
    }

    print(f"data: {data}")


    


    # post data diary 
    try:
        response = requests.post(
            url,
            json = data,
            verify=False)


        # request success
        if(response.status_code == 200):
            print(response.status_code,response.text)
        
        # fail
        else:
            print(response.status_code,response.text)


    except Exception as e:
        print("An error ouccured : ",e)  



def main():

    play_wav_file(f'/home/{username}/yykc/loading.wav')

    try:
        while True:
            if switch.locker_switch.is_pressed:
                print("Switch ON")
                process()
            else:
                print("Switch OFF")
            time.sleep(1)  # 1초 간격으로 스위치 상태 확인

    except KeyboardInterrupt:
        
        print("Program stopped by User")






    









if __name__ == "__main__":
    main()
