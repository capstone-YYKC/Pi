
import pygame

# text 입력에 GPT API 불러오면 됨.
text = "안녕하세요"

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

if __name__ == '__main__':
    tts = gTTS(
        text=text,
        lang='ko', slow=False
    )
    tts.save('example.wav')

# WAV 파일 경로 설정
wav_file_path = "example.wav"

# WAV 파일 재생
play_wav_file(wav_file_path)

