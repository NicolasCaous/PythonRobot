from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

#Opcoes da picamera
camera = PiCamera()  #205, 154
camera.resolution = (208, 160)
camera.framerate = 30
rawCapture = PiRGBArray(camera)

#Opcoes de gravacao
gravar = False

fps = 15
capSize = (256,256)
fourcc = cv2.cv.CV_FOURCC('X','V','I','D')
out = cv2.VideoWriter('output.avi',fourcc,fps,capSize,True)

#Deixa a camera aquecer
time.sleep(0.1)

print("INICIANDO CAMERA")

#looping principal
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	#Transforma imagem da picamera em array
	image = frame.array
	#Trata a imagem para preto e branco
	##image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 
	#Mostra as duas imagens
	cv2.imshow("COLORIDO", image)
	##cv2.imshow("PRETO E BRANCO", image_gray)

	#Gravando frame
	if(gravar):
		out.write(image)	

	#Le a tecla pressionada
	key = cv2.waitKey(1) & 0xFF
 	
	#Reset RawCapture // nao funciona sem zerar o array
	rawCapture.truncate(0)

	#Sair ao pressionar 'q'
	if key == ord("q"):
		break

#Seguranca
out.release()
cv2.destroyAllWindows()
