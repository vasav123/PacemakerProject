import serial
import time
import struct

packets = [0x16,0x00,0x00,0x01]


ser = serial.Serial(port = "/dev/ttyACM0", baudrate = 115200)

ser.flush()
while True:
	packets[1] = 0x00
	ser.write(bytearray(packets))
	time.sleep(1)
	packets[1] = 0x01
	ser.write(bytearray(packets))
	time.sleep(1)
	print(struct.unpack('>BBB',ser.read(size= 3)))

ser.close()

