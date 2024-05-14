# from bert.predict_emotion import predict
from ai_api.create_comment import CreateComment
from stt.stt import SpeechToText




def main():
    # predict : 다이어리를 인풋으로 넣으면 {'행복': 0.014690425, '중립': 0.89617246, '분노': 0.011883826, '슬픔': 0.07725335} 과 같은 감정 예측값 리턴
    # emotion = predict("안녕하세요.")
    # print(emotion)

    #CreateComment: 다이어리를 인풋으로 넣으면 comment를 리턴
    # comment = CreateComment("안녕하세요.")
    # print(comment)

    SpeechToText()





if __name__ == "__main__":
    main()