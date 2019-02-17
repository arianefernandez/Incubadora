from miband2 import MiBand2
from apscheduler.schedulers.blocking import BlockingScheduler
from emocion import predecirEmocion
import threading
import time

def obtenerEmocion():
    emocion = predecirEmocion()
    emocion.fotografiar()
    emocion.predict()
    
def Hilo1():
    scheduler = BlockingScheduler()
    scheduler.add_job(obtenerEmocion, 'interval', minutes=15)
    scheduler.start()


def Hilo2():
    print('Connecting')
    band = MiBand2('FA:01:FB:63:6A:75')
    band.setSecurityLevel(level="medium")
    
    band.authenticate()
    band.init_after_auth()
    
    print("Cont. HRM start")
    band.hrmStopContinuous()
    band.hrmStartContinuous()
    while True:
        band.char_hrm_ctrl.write(b'\x16', True)
        band.waitForNotifications(1.0)
    
    print("Disconnecting...")
    band.disconnect()
    del band
    
if __name__ == "__main__":
    h=threading.Thread(target=Hilo1)
    h2=threading.Thread(target=Hilo2)
    h.start()
    h2.start()
   


