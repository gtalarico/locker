#!
# Raspberry Pi x
# Setup
# BCM
# Keypad 1x4


import RPi.GPIO as rpi
rpi.setmode(rpi.BCM)
#rpi.setmode(rpi.BOARD)

import time
print 'rpi Ready'

ports = [21,22,23,24]
for n, port in enumerate(ports):
    rpi.setup(port, rpi.IN, pull_up_down=rpi.PUD_DOWN)

def get_keypress():
    for n, port in enumerate(ports):
        if rpi.input(port):
            return n + 1

rpi.setup(5, rpi.OUT)

def blink_up():
    rpi.output(5, 1)

def blink_down():
    rpi.output(5, 0)

def get_digit():
    while True:
        digit = get_keypress()
        if digit:
            print 'key press detected: ', digit
            blink_up()
            while get_keypress():
                pass
            blink_down()
            print 'key released.'
            break
        else:
            continue
    return digit

PID = []

try:
    while True:

        print 'Please enter 4 digit pin: '

        for i in range(4):
            PID.append(get_digit())
            print PID

        print 'PID: ', PID
        PID = []


except KeyboardInterrupt:
    rpi.cleanup()
    print 'Exiting... rpi cleanned'

# rpi.cleanup()
