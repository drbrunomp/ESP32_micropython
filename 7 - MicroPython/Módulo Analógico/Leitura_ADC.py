from machine import Pin, ADC
import time

sensor = ADC(Pin(32))
led = Pin(2, Pin.OUT)

while True:    
    sensor.atten(ADC.ATTN_11DB)
    tensao = sensor.read() * 0.0008058608
    print("SENSOR (V) : ",tensao)
    
    
    if tensao <= 3.0:
        led.on()
        time.sleep_ms(500)
        led.off()
        time.sleep_ms(500)
    else:
        led.off()
    