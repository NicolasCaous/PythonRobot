from utils import *
import traceback
import time
import cv2

piv = PiVideoStream((208,160), 32).start()
time.sleep(2.0)

try:
	while(True):
		frame = piv.PID([10, 198, 4], [145, 125, 105, 85, 65], 255, 2, 10)
		cv2.imshow("TESTE", frame)
	
		key = cv2.waitKey(1) & 0xFF
		if(key == ord("q")):
			break

except:
	traceback.print_exc()
	pass

cv2.destroyAllWindows()
piv.stop()
