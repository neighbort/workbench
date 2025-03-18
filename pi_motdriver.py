import pigpio
from time import sleep

pi = pigpio.pi()

pin_ain1 = 22
pin_ain2 = 27
pin_bin1 = 10
pin_bin2 = 17

def test_motor(pin1, pin2):
    pi.set_mode(pin1, pigpio.OUTPUT)
    pi.set_mode(pin2, pigpio.OUTPUT)
    pi.write(pin1, 1)
    sleep(0.5)
    pi.write(pin1, 0)
    sleep(0.5)
    pi.write(pin2, 1)
    sleep(0.5)
    pi.write(pin2, 0)

#test_motor(pin_ain1, pin_ain2)
test_motor(pin_bin1, pin_bin2)
