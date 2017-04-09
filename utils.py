from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
import cv2

class PiVideoStream:
	font = cv2.FONT_HERSHEY_SIMPLEX
	def __init__(self, resolution=(208,160), framerate=32):
		self.camera = PiCamera()
		self.camera.resolution = resolution
		self.camera.framerate = framerate
		self.rawCapture = PiRGBArray(self.camera, size=resolution)
		self.stream = self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True)
		self.frame = None
		self.stopped = False
	
	def start(self):
		Thread(target=self.update, args=()).start()
		return self

	def update(self):
		for f in self.stream:
			self.frame = f.array
			self.rawCapture.truncate(0)
			
			if(self.stopped):
				self.stream.close()
				self.rawCapture.close()
				self.camera.close()
				return

	def read(self):
		return self.frame

	def stop(self):
		self.stopped = True

	def PID(self, linha, pidvalues, target, clmin, clmax):
		f_bgr = self.frame
		f_bw = cv2.cvtColor(f_bgr, cv2.COLOR_BGR2GRAY)
		ret, mask = cv2.threshold(f_bw, 50, 255, cv2.THRESH_BINARY_INV)
		curva = 0
       		for i in pidvalues:
                	tmp = centroLinha(mask[i, linha[0]:linha[1]:linha[2]], clmin, clmax, target, linha[0], linha[2])
			cv2.circle(f_bgr, (tmp, i), 10, (0,255,0), 2)
                	if(tmp != 0):
                        	curva = curva + tmp - 104
		cv2.putText(f_bgr, str(curva), (90, 20), self.font, 0.8, (0,255,0), 2, cv2.CV_AA)
		return f_bgr

	def PIDraw(self, linha, pidvalues, target, clmin, clmax):
                f_bgr = self.frame
                f_bw = cv2.cvtColor(f_bgr, cv2.COLOR_BGR2GRAY)
                ret, mask = cv2.threshold(f_bw, 50, 255, cv2.THRESH_BINARY_INV)
                curva = 0
                for i in pidvalues:
                        tmp = centroLinha(mask[i, linha[0]:linha[1]:linha[2]], clmin, clmax, target, linha[0], linha[2])
                        if(tmp != 0):
                                curva = curva + tmp - 104
                return curva

def centroLinha(linha, menor, maior, preto, init, step):
	res = 0
	soma = 0
	pos = init
	npreto = 0
	for pixel in linha:
		if(pixel == preto):
			soma = soma + pos
			npreto = npreto + 1
		elif(npreto != 0):
			soma = soma / npreto
			if(soma > res and npreto >= menor and npreto <= maior):
				res = soma
			soma = 0
			npreto = 0
		pos = pos + step
	if(npreto != 0):
		soma = soma / npreto
		if(soma > res and npreto >= menor and npreto <= maior):
			res = soma
	return res
