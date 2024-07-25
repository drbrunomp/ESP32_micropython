from machine import Pin
from time import sleep
import dht

sensor = dht.DHT11(Pin(12))

while True:
    try:       
       sensor.measure()
       temp = sensor.temperature()
       umid = sensor.humidity()
       print("Temperatura (C):", temp)
       print("Umidade (%):", umid)
       sleep(1)
    except OSError as err:
        print("FALHA !!!")
    
