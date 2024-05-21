import bert.predict_emotion
import bart.kobart
import switch
from ai_api.create_comment import CreateComment
from stt.stt import SpeechToText
from tts.tts import PrintComment
from tts.tts import play_wav_file
import requests

import time

from username import username





def process():

    # 1. STT
    # SppechToText : 마이크 입력을 text로 리턴
    content = SpeechToText()
    print(f"사용자 입력: {content}")

    # 2. 요약
    summarization = bart.kobart.summarization(content)

    # 3. 코멘트 생성 및 출력
    #CreateComment: 다이어리를 인풋으로 넣으면 comment를 리턴
    comment = CreateComment(summarization) # 사용자에게 출력할 코멘트
    print(f"comment: {comment}")
    PrintComment(comment)


    # 4. 감정 예측
    # predict : 
    # 다이어리를 인풋으로 넣으면 {'행복': 0.014690425, '중립': 0.89617246, '분노': 0.011883826, '슬픔': 0.07725335} 과 같은 
    # 감정 예측값 리턴
    emotion = bert.predict_emotion.predict(content)      # 감정 예측값
    emotion_score = round(bert.predict_emotion.calculate_emotion_score(emotion),2)

    # 5. 서버로 전송
    url  = 'https://100.27.127.192:3000/diary'

    # # transcribe_streaming_mic redirection data
    # # diary content 

    data = {
        'userIdx' : 3,                  # 유저구분
        'emotionStatus' : max(emotion, key=emotion.get),        # 감정
        'emotionScore' : emotion_score,          # 감정점수
        'content': content,              # 일기
        'consolation': comment,       # 생성된 코멘트
        'summarize': summarization      # 요약
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