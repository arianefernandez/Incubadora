from spidev import SpiDev

class MCP3008:
    def __init__(self, bus = 0, device = 0):
        self.bus, self.device = bus, device
        self.spi = SpiDev()
        self.abrir()

    def abrir(self):
        self.spi.open(self.bus, self.device)
    
    def leer(self, channel):
        if ((channel > 7) or (channel < 0)):
            return -1
        self.spi.max_speed_hz = 1350000
        adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
        return data
            
    def cerrar(self):
        self.spi.close()
