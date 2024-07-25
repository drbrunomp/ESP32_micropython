from machine import TouchPad, Pin
from time import sleep

sensor = TouchPad(Pin(4))
led = Pin(2,Pin.OUT)

while True:
    sn_cap = sensor.read()
    print(sn_cap)
    if sn_cap > 400:
        led.on()
    else:
        led.off()
        
    