import pigpio
from time import sleep

gpio = pigpio.pi()
pin = 12
gpio.set_mode(pin, pigpio.INPUT)

def WithPullUp(pin):
    gpio.set_pull_up_down(pin, pigpio.PUD_UP)
    cite = {1 : "Switch Free", 0 : "Switch Pushed"}
    print("Start!")
    try:
        while True:
            switch = gpio.read(pin)
            print(switch, cite[switch])
            sleep(0.5)
    except KeyboardInterrupt:
        gpio.set_pull_up_down(pin, pigpio.PUD_OFF)
        print("Finish!")

def WithPullDown(pin):
    gpio.set_pull_up_down(pin, pigpio.PUD_DOWN)
    cite = {0 : "Switch Free", 1 : "Switch Pushed"}
    print("Start!")
    try:
        while True:
            switch = gpio.read(pin)
            print(switch, cite[switch])
            sleep(0.5)
    except KeyboardInterrupt:
        gpio.set_pull_up_down(pin, pigpio.PUD_OFF)
        print("Finish!")


WithPullUp(pin)
#WithPullDown(pin)
