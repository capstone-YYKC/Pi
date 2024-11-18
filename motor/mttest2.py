import RPi.GPIO as GPIO
from time import sleep

# GPIO 핀 번호 설정
L_SHOULDER_PIN = 18
R_SHOULDER_PIN = 13
L_ARM_PIN = 23
R_ARM_PIN = 19
HEAD_PIN = 12

# GPIO 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(L_SHOULDER_PIN, GPIO.OUT)
GPIO.setup(R_SHOULDER_PIN, GPIO.OUT)
GPIO.setup(L_ARM_PIN, GPIO.OUT)
GPIO.setup(R_ARM_PIN, GPIO.OUT)
GPIO.setup(HEAD_PIN, GPIO.OUT)

# PWM 주파수 설정
PWM_FREQ = 50  # 서보 모터의 PWM 주파수 (50Hz)
l_shoulder_pwm = GPIO.PWM(L_SHOULDER_PIN, PWM_FREQ)
r_shoulder_pwm = GPIO.PWM(R_SHOULDER_PIN, PWM_FREQ)
l_arm_pwm = GPIO.PWM(L_ARM_PIN, PWM_FREQ)
r_arm_pwm = GPIO.PWM(R_ARM_PIN, PWM_FREQ)
head_pwm = GPIO.PWM(HEAD_PIN, PWM_FREQ)

# PWM 시작 (0도에서 시작)
l_shoulder_pwm.start(0)
r_shoulder_pwm.start(0)
l_arm_pwm.start(0)
r_arm_pwm.start(0)
head_pwm.start(0)

def deactivate_servo(pwm):
    """지정된 서보 모터를 비활성화"""
    pwm.ChangeDutyCycle(0)  # 모터에 신호를 끊음

def activate_servo(pwm, angle):
    """지정된 서보 모터를 활성화하고 원하는 위치로 이동"""
    duty_cycle = angle_to_duty_cycle(angle)
    pwm.ChangeDutyCycle(duty_cycle)

def activate_servo_slowly(pwm, start_angle, target_angle, step=1, delay=0.05):
    """지정된 서보 모터를 천천히 이동"""
    if start_angle < target_angle:
        for angle in range(start_angle, target_angle + step, step):
            duty_cycle = angle_to_duty_cycle(angle)
            pwm.ChangeDutyCycle(duty_cycle)
            sleep(delay)
    else:
        for angle in range(start_angle, target_angle - step, -step):
            duty_cycle = angle_to_duty_cycle(angle)
            pwm.ChangeDutyCycle(duty_cycle)
            sleep(delay)

def angle_to_duty_cycle(angle):
    """각도를 PWM의 듀티 사이클로 변환 (0도 ~ 180도)"""
    return 2 + (angle / 18)  # 듀티 사이클 변환

def nodding(stop_event):
    """머리 끄덕임 동작"""
    try:
        while not stop_event.is_set():
            activate_servo_slowly(head_pwm, 0, 54, step=3, delay=0.05)
            print("Head value = 54")
            sleep(0.2)
            activate_servo_slowly(head_pwm, 54, 0, step=3, delay=0.05)
            print("Head value = 0")
            sleep(0.2)

    except KeyboardInterrupt:
        print("interrupted")

    finally:
        activate_servo(head_pwm, 0)
        sleep(1)
        deactivate_servo(head_pwm)

def waving_hand(stop_event):
    """손 흔들기 동작"""
    activate_servo(r_arm_pwm, 180)
    sleep(1)
    deactivate_servo(r_arm_pwm)
    try:
        while not stop_event.is_set():
            activate_servo_slowly(r_shoulder_pwm, 180, 110, step=3, delay=0.05)
            print("r_shoulder value = 110")
            sleep(0.2)
            activate_servo_slowly(r_shoulder_pwm, 110, 180, step=3, delay=0.05)
            print("r_shoulder value = 180")
            sleep(0.2)

    except KeyboardInterrupt:
        print("interrupted.")

    finally:
        activate_servo(r_shoulder_pwm, 180)
        activate_servo(r_arm_pwm, 0)
        sleep(2)
        deactivate_servo(r_shoulder_pwm)
        deactivate_servo(r_arm_pwm)

def hug(stop_event):
    """포옹 동작"""

    try:
        activate_servo(l_arm_pwm, 90) 
        activate_servo(r_arm_pwm, 90)  
        sleep(1)
        deactivate_servo(l_arm_pwm)
        deactivate_servo(r_arm_pwm)
        while not stop_event.is_set():
            sleep(1)

    except KeyboardInterrupt:
        print("interrupted")

    finally:
        activate_servo(l_arm_pwm, 180)
        activate_servo(r_arm_pwm, 0)
        sleep(2)
        deactivate_servo(l_arm_pwm)
        deactivate_servo(r_arm_pwm)



# nodding()
# hug()
# waving_hand()
