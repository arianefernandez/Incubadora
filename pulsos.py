import time
import simpleaudio as sa

class reproducirPulso:
	def __init__(self, pulso):
		self.pulso =pulso

	def reproduccionSonido(self):
		if self.pulso < 50:
			self.pulso = 50
		elif self.pulso > 120:
			self.pulso = 120
		elif self.pulso >= 50 and 60 >= self.pulso:
			sonido_wav = sa.WaveObject.from_wave_file("Corazon1.wav")
			ritmo = (1-(self.pulso/60.0))
		elif self.pulso > 60 and self.pulso <= 90:
			sonido_wav = sa.WaveObject.from_wave_file("Corazon2.wav")
			ritmo = (1-(self.pulso/90.0))
		elif self.pulso > 90 and self.pulso <= 120:
			sonido_wav = sa.WaveObject.from_wave_file("Corazon3.wav")
			ritmo = (1-(self.pulso/120.0))
		cont = 0
		while cont < 10:
                    print(self.pulso)
                    sonido_play = sonido_wav.play()
                    sonido_play.wait_done()
                    time.sleep(ritmo)
                    cont = cont + 1



	
