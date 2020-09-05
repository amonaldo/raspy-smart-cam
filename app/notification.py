
import serial
import settings

gsm = serial.Serial('/dev/ttyS0', baudrate=9600)
cmd = 'ATD+ ' + settings.PHONE_NUMBER + ';\r\n'
gsm.write(cmd.encode())
gsm.close()
