import serial
import time

ser = serial.Serial('/dev/ttyACM0', 115200)

while(True):
	s = raw_input('>> ')
	if(s == 'exit'):
		break
	ser.write(str(s))
	out = ''
	time.sleep(0.05)
	while(ser.inWaiting() > 0):
		out = out + ser.read(1)
	if(out != ''):
		print('<< ' + out)
