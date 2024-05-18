
import pygame

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


from gtts import gTTS



def PrintComment(text):
    path = '/home/test01/yykc/tts/comment/recent_comment.wav'
    tts = gTTS(
        text=text,
        lang='ko', slow=False
    )
    tts.save(path)
    play_wav_file(path)



