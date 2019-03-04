from miband2 import MiBand2
from apscheduler.schedulers.blocking import BlockingScheduler
from emocion import predecirEmocion
from pulsos import reproducirPulso
from influxdb import InfluxDBClient
from datetime import datetime
from mcp3008 import MCP3008
import threading
import time

bienestar = True
ruido = 0
luz = 0

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

def obtenerEmocion():
    emocion = predecirEmocion()
    emocion.fotografiar()
    emocion = emocion.predict(ruido)
    global bienestar
    if 'Llanto' in emocion:
        bienestar=False
    else:
        bienestar=True
        
    
def HiloEmociones():
    scheduler = BlockingScheduler()
    scheduler.add_job(obtenerEmocion, 'interval', minutes=2)
    scheduler.start()


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
    mcp = MCP3008(0,0)
    global ruido
    ruido = mcp.leer(0)
    ruido = (ruido + 40.24)/6.26
    ruido = int(ruido)
    print(ruido)
    if(ruido > 60):
        obtenerEmocion()

def obtenerLuz():
    mcp = MCP3008(0,0)
    global luz
    luz = mcp.leer(1)
    print(luz)
        
def HiloRuido():
    scheduler = BlockingScheduler()
    scheduler.add_job(obtenerRuido, 'interval', seconds=5)
    scheduler.start()

def HiloLuz():
    scheduler = BlockingScheduler()
    scheduler.add_job(obtenerLuz, 'interval', seconds=1)
    scheduler.start()
    
def HiloBD():
    while True:
        global ruido
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
            
        ]
        cliente.write_points(data)
    
    
if __name__ == "__main__":
    h=threading.Thread(target=HiloEmociones)
    h2=threading.Thread(target=HiloCorazon)
    h3=threading.Thread(target=HiloRuido)
    h4=threading.Thread(target=HiloBD)
    h5=threading.Thread(target=HiloLuz)
    h.start()
    h2.start()
    h3.start()
    h4.start()
    h5.start()   
