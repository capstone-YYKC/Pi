from gpiozero import Button
import time

# GPIO 핀 번호 설정
# GPIO 17 핀을 input으로 설정.
switch_pin = 17
locker_switch = Button(switch_pin)