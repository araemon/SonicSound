# -*- coding: utf-8 -*-
# このプログラムはpython2で実行すること

import RPi.GPIO as GPIO
import time
import os
import signal

GPIO.setmode(GPIO.BCM)  # 役割ピン番号で命名
TRIG = 20
ECHO = 21
SIG = 26
SERVO_PWM_MIN = 2.2  # 0° 時計の針で9時を0°とする
SERVO_PWM_MAX = 10.8  # 180°
SERVO_PWM_1DEGREE = (SERVO_PWM_MAX - SERVO_PWM_MIN) / 180
MONITORING_DIST = 20  # 物体が存在したとみなす最長距離(cm)

C = 343  # 気温20度での音速(m/s)

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(SIG, GPIO.OUT)

GPIO.output(TRIG, 0)
servo = GPIO.PWM(SIG, 50)
time.sleep(0.3)

servo.start(0)


def readDistance():
    GPIO.output(TRIG, 1)
    time.sleep(0.00001)  # 10μs
    GPIO.output(TRIG, 0)

    while GPIO.input(ECHO) == 0:
        signaloff = time.time()  # 秒
    while GPIO.input(ECHO) == 1:
        signalon = time.time()  # 秒

    t = signalon - signaloff  # 秒
    distance = t * C * 100 / 2
    return distance


def rotate(angle):  # 0° 〜 180°
    pwm = angle * SERVO_PWM_1DEGREE + SERVO_PWM_MIN
    if pwm > SERVO_PWM_MAX:
        pwm = SERVO_PWM_MAX
    elif pwm < SERVO_PWM_MIN:
        pwm = SERVO_PWM_MIN

    servo.ChangeDutyCycle(pwm)
    return


def cleanup():
    print('cleanup')
    rotate(90)
    time.sleep(1)
    servo.stop()
    GPIO.cleanup()


initAngle = 0
currentAngle = 0
clockwise = True
isCatched = False
isMissing = False  # 物体を見失う
isWondering = False  # 不安フラグ
missingCount = 0

try:
    rotate(initAngle)
    time.sleep(1)
    while True:

        dist = readDistance()
        # print('角度: {0}, 距離: {1}'.format(currentAngle, dist))

        isExistObject = dist < MONITORING_DIST

        if isExistObject:
            isMissing = False
            missingCount = 0
            isWondering = False
            if isCatched == False:  # 新規発見！
                isCatched = True
                clockwise = False if clockwise == True else True
        else:
            if isCatched:
                isCatched = False
                clockwise = False if clockwise == True else True
                # print("物体を見逃しますた！")
                isMissing = True

            if isMissing:
                missingCount += 1

        if missingCount > 100:  # 物体が存在しなかったのでリセットする
            isCatched = False
            isWondering = False
            isMissing = False
        elif missingCount > 10:  # 不安フラグを立てる
            isWondering = True

        if isCatched:
            gain = 0.7
        elif isWondering:
            gain = 4
        else:
            gain = 1

        if clockwise:
            gain *= 1
        else:
            gain *= -1

        currentAngle += 1 * gain

        if currentAngle > 180:
            clockwise = False
        elif currentAngle < 0:
            clockwise = True

        rotate(currentAngle)
        time.sleep(0.005)


except KeyboardInterrupt:
    print('KeyboardInterrupt')
except:
    print('other')
finally:
    cleanup()
