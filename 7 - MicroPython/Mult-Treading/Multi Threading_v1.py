import _thread as T
import time
from machine import Pin

led1 = Pin(22,Pin.OUT)
led2 = Pin(23,Pin.OUT)
led3 = Pin(2, Pin.OUT)

def funcao_led1 (string,t):
     led1 = Pin(22,Pin.OUT)

     while True:
        print(string)
        led1.on()
        time.sleep(t)
        led1.off()
        time.sleep(t)
    
def funcao_led2 (string,t):
    led2 = Pin(23,Pin.OUT)

    while True:
        print(string)
        led2.on()
        time.sleep(t)
        led2.off()
        time.sleep(t)
    
def funcao_led3 (string,t):
    led3 = Pin(2, Pin.OUT)

    while True:
       print(string)
       led3.on()
       time.sleep(t)
       led3.off()
       time.sleep(t)
    
try:
        T.start_new_thread (funcao_led1, ("led1",4))
        T.start_new_thread (funcao_led2, ("led2",4))
        T.start_new_thread (funcao_led3, ("led3",4))
        
except:
   print ("Erro: desabilitado para o thread")
        