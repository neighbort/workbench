import pigpio
from time import sleep

port_1 = 23
port_2 = 24
port_3 = 25

pi = pigpio.pi()
pins = [port_1, port_2, port_3]
for pin in pins:
    pi.set_mode(pin, pigpio.OUTPUT)

pi.write(port_1, 1)
sleep(1)
pi.write(port_1, 0)

pi.write(port_2, 1)
sleep(1)
pi.write(port_2, 0)

pi.write(port_3, 1)
sleep(1)
pi.write(port_3, 0)
