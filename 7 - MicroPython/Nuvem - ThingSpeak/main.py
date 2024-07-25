import network, ssd1306
from machine import Pin, I2C
from time import sleep
from dht import DHT11
from umqtt.robust import MQTTClient
import os  #traz informações sobre o sistema operacional.
import gc  #fornece a capacidade de desabilitar o coletor,
           #ajustar a frequência de coleta e definir opções de depuração.
import sys # fornece funções e variáveis ​​usadas para manipular diferentes
           # partes do ambiente de tempo de execução do Python.

i2c = I2C(scl=Pin(22), sda=Pin(21))

i2c = I2C(scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

led = Pin(2, Pin.OUT)

# DHT
dht11 = DHT11(Pin(23))

# Função para ler o sensor DHT
def LeituraDht():
    dht11.measure()
    return dht11.temperature(), dht11.humidity()

# Função para ler vários dados (você poderia estar usando um outro sensor em conjunto)
def ColetaDados():
    temp, hum = LeituraDht()
    return temp, hum
   
# criando uma função para o led piscar indicando que o programa está rodando
def PiscaLed(num):
    for i in range(0, num):
        led.on()
        sleep(0.5)
        led.off()
        sleep(0.5)
        

# WiFi SSID (Service Set Identifier) & Senha (Password)
wifiSSID = 'O NOME DA SUA REDE'
wifiPassword = 'A SUA SENHA'

# Desliga o Ponto de Acesso (Configuração padrão do ESP32).
ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)

# Conecta o ESP32 à rede WiFi no Modo Estação (Station) 
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(wifiSSID, wifiPassword)

# Aguarda o ESP32 estar conectado à rede WiFi por alguns segundos
MAX_ATTEMPTS = 10
attempt_count = 0
while not wifi.isconnected() and attempt_count < MAX_ATTEMPTS:
    attempt_count += 1
    sleep(1)

if attempt_count == MAX_ATTEMPTS:
    print('Nao pode ser conectado na rede WiFi')
    sys.exit()
  
# cria um clientID MQTT aleatório (randômico) 
randomNum = int.from_bytes(os.urandom(3), 'little')
myMqttClient = bytes("client_"+str(randomNum), 'utf-8')

# Conecta ao Thingspeak MQTT broker
# Conexão TCP (port 1883) - Não oferece segurança.
# Para uma conexão segura utilizaremos TLS (Transport Layer Security) - protocolo de criptografia 
#   Ajustando o parâmetro inicializador MQTTClient para "ssl=True" - SSL (Secure Sockets Layer)
#   Observação: Uma conexão segura utiliza aproximadamente 9 kB da pilha de memória RAM.
         
THINGSPEAK_URL = b"mqtt.thingspeak.com" 
THINGSPEAK_USER_ID = b'O seu nome de usuário no ThingSpeak' #A sua identificação de usuário no ThingSpeak
THINGSPEAK_MQTT_API_KEY = b'API MQTT do seu canal' #Chave API MQTT do seu canal no ThingSpeak
client = MQTTClient(client_id=myMqttClient, 
                    server=THINGSPEAK_URL, 
                    user=THINGSPEAK_USER_ID, 
                    password=THINGSPEAK_MQTT_API_KEY, ssl=False)
                    
try:            
    client.connect()
except Exception as e:
    print('Nao pode ser conectado ao MQTT server {}{}'.format(type(e).__name__, e))
    sys.exit()

# Publicando os dados no Canal gratuito do ThingSpeak
THINGSPEAK_CHANNEL_ID = b'ID do seu canal' #ID do seu Canal ThingSpeak
THINGSPEAK_CHANNEL_WRITE_API_KEY = b'A API_KEY do seu canal - chave de escrita' #A sua chave de Escrita 
PUBLISH_PERIOD_IN_SEC = 2 #Escrevendo dados a cada 2 segundos
while True:
    try:
        led.on()
        temperatura, umidade = ColetaDados()
        led.off()         
        PiscaLed(3)
        
        oled.fill(0)
        oled.text("Temperatura",20,5)
        oled.text(str(temperatura),40,20)
        oled.text("*C", 60,20)
        oled.text("Umidade",30,40)
        oled.text(str(umidade),40,55)
        oled.text("%", 60,55)
        oled.show()
        
        #freeHeapInBytes = gc.mem_free()
        credentials = bytes("channels/{:s}/publish/{:s}".format(THINGSPEAK_CHANNEL_ID, THINGSPEAK_CHANNEL_WRITE_API_KEY), 'utf-8')  
        #payload = bytes("field1={:.1f}\n".format(freeHeapInBytes), 'utf-8')
        payload = bytes("field1="+str(temperatura)+"&field2="+str(umidade), 'utf-8')
        client.publish(credentials, payload)
        sleep(PUBLISH_PERIOD_IN_SEC)
        print('Temperatura=', temperatura, 'C', 'Umidade=', umidade, '%')
        
    except KeyboardInterrupt:
        print('Ctrl-C pressionado!!! O ESP32 foi desconectado da rede WiFi')
        client.disconnect()
        sys.exit()
        
       

