
import serial
import time
import settings


commands = [
	'AT',
	'AT+CPIN=' + settings.SIM_CARD_PIN,
	'AT+CBAND="ALL_BAND"',
	'AT+CMGF=1'
]

gsm = serial.Serial('/dev/ttyS0', baudrate=9600)

for cmd in commands:
	gsm.write((cmd + '\r\n').encode())
	time.sleep(5)
	
gsm.close()
