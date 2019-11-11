# -*- coding: utf-8 -*-
# python2で実行すること

import RPi.GPIO as GPIO
import time
import os
import signal


GPIO.setmode(GPIO.BCM)
SIG = 26
GPIO.setup(SIG, GPIO.OUT)


# PWMサイクル:20ms(=50Hz)
servo = GPIO.PWM(SIG, 50)
time.sleep(0.3)

servo.start(0)
servo.ChangeDutyCycle(6.3)  # 0°
time.sleep(1.0)


for i in range(5):
    servo.ChangeDutyCycle(2.2)  # 0°
    time.sleep(0.7)

    # servo.ChangeDutyCycle(10.8)  # 180°
    # time.sleep(0.7)

    # servo.ChangeDutyCycle(7.25)
    # time.sleep(0.5)

    # servo.ChangeDutyCycle(12)
    # time.sleep(0.5)

    # servo.ChangeDutyCycle(7.25)
    # time.sleep(0.5)

# servo.ChangeDutyCycle(6.3)  # 90°
time.sleep(1.0)

servo.stop()
GPIO.cleanup()
