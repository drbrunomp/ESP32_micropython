import _thread as T
import time
from machine import Pin

def funcao_led (pino, t):
    time.sleep(1)
    led = Pin(pino,Pin.OUT)

    while True:
       print("led ",pino)
       led.on()
       time.sleep(t)
       led.off()
       time.sleep(t)
       
try:
        T.start_new_thread (funcao_led, (2,4))
        T.start_new_thread (funcao_led, (22,4))
        T.start_new_thread (funcao_led, (23,4))
        
except:
   print ("Erro: desabilitado para o thread")
        