# from bert.predict_emotion import predict
import bert.predict_emotion
import switch
from ai_api.create_comment import CreateComment
from stt.stt import SpeechToText
from tts.tts import PrintComment
import requests

import time






def process():
    # SppechToText : 마이크 입력을 text로 리턴
    content = SpeechToText()
    print(f"사용자 입력: {content}")

    #CreateComment: 다이어리를 인풋으로 넣으면 comment를 리턴
    comment = CreateComment(content) # 사용자에게 출력할 코멘트
    print(f"comment: {comment}")
    PrintComment(comment)

    # predict : 
    # 다이어리를 인풋으로 넣으면 {'행복': 0.014690425, '중립': 0.89617246, '분노': 0.011883826, '슬픔': 0.07725335} 과 같은 
    # 감정 예측값 리턴
    emotion = bert.predict_emotion.predict(content)      # 감정 예측값


    # url  = 'http://18.211.120.39:3000/diary'

    # # transcribe_streaming_mic redirection data
    # # diary content 

    # data = {
    #     'userIdx' : 3,                  # 유저구분
    #     'emotionStatus' : "sad",        # 감정
    #     'emotionScore' : 11.2,          # 감정점수
    #     'content': content,              # 일기
    #     'consolation': 'ㄴㄴㄴㄴㄴㄴㄴㄴ'       # 생성된 코멘트
    #     'summarize': 'ssssssss'
    # }


    # # post data diary 
    # try:
    #     response = requests.post(url,json = data)

    #     # request success
    #     if(response.status_code == 200):
    #         print(response.status_code,response.text)
        
    #     # fail
    #     else:
    #         print(response.status_code,response.text)

    # except Exception as e:
    #     print("An error ouccured : ",e)    



def main():
    try:
        while True:
            if switch.locker_switch.is_pressed:
                print("Locker switch is pressed")
                process()
            else:
                print("Locker switch is not pressed")
            time.sleep(1)  # 1초 간격으로 스위치 상태 확인

    except KeyboardInterrupt:
        print("Program stopped by User")






    









if __name__ == "__main__":
    main()