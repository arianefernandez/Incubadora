from miband2 import MiBand2

def main():
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
    main()


