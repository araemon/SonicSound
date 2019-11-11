# -*- coding: utf-8 -*-
# python2で実行すること

import RPi.GPIO as GPIO
import time
import os
import signal


GPIO.setmode(GPIO.BCM)
TRIG = 20
ECHO = 21
C = 343  # 気温20度の時の音速(m/s)

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.output(TRIG, 0)
time.sleep(0.3)


def readDistance():
    GPIO.output(TRIG, 1)
    time.sleep(0.00001)  # 10μs
    GPIO.output(TRIG, 0)

    while GPIO.input(ECHO) == 0:
        signaloff = time.time()
    while GPIO.input(ECHO) == 1:
        signalon = time.time()

    t = signalon - signaloff
    distance = t * C * 100 / 2
    return distance


def cleanup():
    print('cleanup')
    GPIO.cleanup()


try:
    while True:
        dist = readDistance()
        print(dist)
        time.sleep(0.1)


except KeyboardInterrupt:
    # SIGINTを監視していれば不要
    print('KeyboardInterrupt')
except:
    print('other')
finally:
    # 終了処理
    cleanup()
