import serial
import time
import struct

packets = [0x16,0x00,0x00,0x01]
counter = 0

ser_found = True
while ser_found:
#	print(counter,"/dev/ttyACM"+str(counter),ser_found)
	if counter > 256:
		print("check vm")
		ser_found = False
	try:
		ser = serial.Serial(port = "/dev/ttyACM"+str(counter), baudrate = 115200)
		ser_found = False
	except:
		counter+=1

ser.flush()
while True:
	# packets[1] = 0x00
	# ser.write(bytearray(packets))
	# time.sleep(1)
	# packets[1] = 0x01
	# ser.write(bytearray(packets))
	# time.sleep(1)
	# print(ord(ser.read(size =1)))
	while (ord(ser.read(size =1)) == 22):
		bytes_array = list(struct.unpack('<h', ser.read(size = 2)))
		print(bytes_array[0])
		# print((bytes_array[0]**2 + bytes_array[1]**2 + bytes_array[2]**2)**(1.0/2))
	# time.sleep(1)

ser.close()

