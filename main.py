from bert.predict_emotion import predict
from ai_api.create_comment import CreateComment
from stt.stt import SpeechToText
from tts.tts import PrintComment




def main():

    # SppechToText : 마이크 입력을 text로 리턴
    diary = SpeechToText()
    content = " ".join(diary)       # 사용자의 입력

    # predict : 
    # 다이어리를 인풋으로 넣으면 {'행복': 0.014690425, '중립': 0.89617246, '분노': 0.011883826, '슬픔': 0.07725335} 과 같은 
    # 감정 예측값 리턴
    emotion = predict(content)      # 감정 예측값

    #CreateComment: 다이어리를 인풋으로 넣으면 comment를 리턴
    comment = CreateComment(content) # 사용자에게 출력할 코멘트
    print(f"comment: {comment}")
    
    PrintComment(comment)

    









if __name__ == "__main__":
    main()