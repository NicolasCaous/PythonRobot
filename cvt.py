from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
from utils import *

#Opcoes opencv
font = cv2.FONT_HERSHEY_SIMPLEX

#Opcoes do algoritmo
clmin = 10
clmax = 50

#Opcoes da picamera
camera = PiCamera()  #205, 154
camera.resolution = (208, 160)
camera.framerate = 20
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

umavez = True

#looping principal
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	#Transforma imagem da picamera em array
	image = frame.array
	#Trata a imagem para preto e branco
	image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	#Filtros                  transforma <200 em 255
	ret, mask = cv2.threshold(image_gray, 50, 255, cv2.THRESH_BINARY_INV)

	#Inverte preto e branco
	mask = cv2.bitwise_not(mask)

	#recorta a parte da imagem original
	##image_gray = cv2.bitwise_and(image_gray, image_gray, mask=mask)

	#Desenhando retangulo                                      #grossua linha
	for i in [60, 80, 100, 120, 140]:
		cv2.rectangle(image, (10,i), (198,i + 10), (0,255,0), 2)

	curva = 0
	#aplicando algoritmo
	for i in [145, 125, 105, 85, 65]:
		tmp = centroLinha(mask[i, 10:198], clmin, clmax)
		cv2.circle(image, (centroLinha(mask[i, 10:198], clmin, clmax), i), 10, (0,255,0), 2)
		if(tmp != 0):
			curva = curva + tmp - 104

	cv2.putText(image, str(curva), (90, 20), font, 0.8, (0,255,0), 2, cv2.CV_AA)
 
	#Mostra as duas imagens
	cv2.imshow("CONTROLE", image)
	##cv2.imshow("PRETO E BRANCO /c FILTRO", mask)

	#if para testes
	if(umavez):
		umavez = False

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
camera.close()
out.release()
cv2.destroyAllWindows()
