#!
# Raspberry Pi x
# Setup
# BCM
# Keypad 1x4

import RPi.GPIO as rpi
import time

#setup
ports = [21,22,23,24]

def pi_init():
    rpi.setmode(rpi.BCM)
    #rpi.setmode(rpi.BOARD)

    print 'rpi Ready'

    for n, port in enumerate(ports):
        rpi.setup(port, rpi.IN, pull_up_down=rpi.PUD_DOWN)

    rpi.setup(5, rpi.OUT)


def pi_cleanup():
    rpi.cleanup()

def get_keypress():
    for n, port in enumerate(ports):
        if rpi.input(port):
            return n + 1

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
            print 'key released: ', digit
            break
    return digit


def get_pin(length):
    pi_init()
    try:
        pin = []
        print 'Please enter your pin ({})'.format(length)
        for i in range(length):
            pin.append(get_digit())
            print pin

        print 'PIN: ', pin
        pi_cleanup()
        # pin is list of ints [1,2,3] etc. Convert to string '123'
        pin = [str(i) for i in pin]
        str_pin = ''.join(pin)
        return str_pin


    except KeyboardInterrupt:
        rpi.cleanup()
        print 'Exiting... rpi cleanned'
        return None
