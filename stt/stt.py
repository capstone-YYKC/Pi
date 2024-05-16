import switch

# [START speech_transcribe_streaming_mic]

import queue
import re
import sys
import datetime


from google.cloud import speech

import pyaudio

import wave
import time


# 녹음파일을 stt api
def stt_api(file_path):

  

    client = speech.SpeechClient()
    with open(file_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="ko-KR",
    )

    transcript = ""

    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        transcript += result.alternatives[0].transcript + " "

    return transcript


    


# 음성녹음하여 저장
def record_audio(filepath, channels=1, rate=16000, chunk=1024):

    audio = pyaudio.PyAudio()

    stream = audio.open(format=pyaudio.paInt16,
                        channels=channels,
                        rate=rate,
                        input=True,
                        frames_per_buffer=chunk)

    print("Recording...")

    frames = []

    while switch.locker_switch.is_pressed:
        data = stream.read(chunk)
        frames.append(data)

    print("Recording stopped.")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    with wave.open(filepath, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))

    print(f"Audio saved to {filepath}")





def SpeechToText():
    path = "/home/test01/yykc/stt/diary/diary.wav"
    record_audio(filepath = path)
    return stt_api(path)