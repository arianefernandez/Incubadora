from miband2 import MiBand2
from apscheduler.schedulers.blocking import BlockingScheduler
from emocion import predecirEmocion
from pulsos import reproducirPulso
from influxdb import InfluxDBClient
from datetime import datetime
from mcp3008 import MCP3008
import RPi.GPIO as GPIO
import threading
import time
import sys
import Adafruit_DHT

mcp = MCP3008(0,0)

pinR = 17
pinR2 = 27
pinA = 18
pinDHT = 4
sensor = 11

bienestar = True
ruido = 0
luz = 0
concentracion = 0
temperatura = 0
humedad = 0

inicio = 0
tiempo = 30000
milis = 0
duracion = 0
ocupacion = 0
ratio = 0

host = 'localhost'
puerto = 8086

cliente = InfluxDBClient(host, puerto)

try:
    cliente.switch_database('incubadora')
    print("Cambiado a BD Incubadora ")
except:
    cliente.create_database('incubadora')
    cliente.switch_database('incubadora')
    print("Creada BD Incubadora y cambiada")
    
		
def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    global pinA
    global pinR
    GPIO.setup(pinA, GPIO.IN)
    GPIO.setup(pinR, GPIO.OUT)
    

def HiloCalidadAire():
    while True:
        global duracion
        duracion = GPIO.input(pinA)
        global ocupacion
        ocupacion = ocupacion + duracion
        
        global inicio
        global tiempo
        global milis
        milis = int(round(time.time() * 1000))
        
        if(milis-inicio > tiempo):	
            global ratio
            ratio = ocupacion/(tiempo*10.0)
            global concentracion
            concentracion = 1.1*pow(ratio,3)-3.8*pow(ratio,2)+520*ratio+0.62
            concentracion = int(concentracion)
            ocupacion = 0
            inicio = milis

def obtenerEmocion():
    emocion = predecirEmocion()
    emocion.fotografiar()
    emocion = emocion.predict(ruido)
    global bienestar
    if 'Llanto' in emocion:
        bienestar=False
    else:
        bienestar=True
        
def HiloCorazon():
    print('Connecting')
    band = MiBand2('FA:01:FB:63:6A:75')
    band.setSecurityLevel(level="medium")
    
    band.authenticate()
    band.init_after_auth()
    
    print("Cont. HRM start")
    band.hrmStopContinuous()
    band.hrmStartContinuous()

    global bienestar
    musica = reproducirPulso(0)
    while True:
        while bienestar:
            band.char_hrm_ctrl.write(b'\x16', True)
            band.waitForNotifications(1.0)
        musica.reproducirMusica()
    
    print("Disconnecting...")
    band.disconnect()
    del band
    
def obtenerRuido():
    global mcp
    global ruido
    ruido = mcp.leer(0)
    ruido = (ruido + 192.8) / 10.94
    ruido = int(ruido)
    if(ruido > 60):
        obtenerEmocion()

def obtenerLuz():
    global mcp
    global luz
    luz = mcp.leer(1)
    luz = (luz * 207) / 618
    luz = int(luz)
  
def HiloERLT():
    scheduler = BlockingScheduler()
    scheduler.add_job(obtenerEmocion, 'interval', minutes=2)
    scheduler.add_job(obtenerTemperaturaHumedad, 'interval', seconds=30)
    scheduler.add_job(obtenerRuido, 'interval', seconds=20)
    scheduler.add_job(obtenerLuz, 'interval', seconds=10)
    scheduler.start()

def obtenerTemperaturaHumedad():
    global pinR
    global humedad
    global temperatura
    
    humedad, temperatura = Adafruit_DHT.read_retry(sensor, pinDHT)
    humedad = int(humedad)
    temperatura = int(temperatura)
    
    if(temperatura<37):
        GPIO.output(pinR, GPIO.LOW)
    else:
        GPIO.output(pinR, GPIO.HIGH)
        
    #if(humedad>70):
        #GPIO.output(pinR2, GPIO.HIGH)
    #else:
        #GPIO.output(pinR2, GPIO.LOW)

def HiloBD():
    while True:
        global ruido
        global luz
        global concentracion
        global temperatura
        global humedad
        global cliente
        data = [
            {
              "measurement": "ruido",
              "tags": {
              },
              "time": datetime.utcnow(),
              "fields": {
                "value" : ruido,
                }
            },
            {
              "measurement": "luz",
              "tags": {
              },
              "time": datetime.utcnow(),
              "fields": {
                "value" : luz,
                }
            },
             {
              "measurement": "calidadAire",
              "tags": {
              },
              "time": datetime.utcnow(),
              "fields": {
                "value" : concentracion,
                }
            },    
             {
              "measurement": "temperatura",
              "tags": {
              },
              "time": datetime.utcnow(),
              "fields": {
                "value" : temperatura,
                }
            },
             {
              "measurement": "humedad",
              "tags": {
              },
              "time": datetime.utcnow(),
              "fields": {
                "value" : humedad,
                }
            },
            
        ]
        cliente.write_points(data)
    
if __name__ == "__main__":
    try:
        setup()
        h=threading.Thread(target=HiloERLT)
        h2=threading.Thread(target=HiloCorazon)
        h3=threading.Thread(target=HiloBD)
        h4=threading.Thread(target=HiloCalidadAire)
        h.start()
        h2.start()
	h3.start()
	h4.start()
    
