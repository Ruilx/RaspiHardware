#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, time
from datetime import datetime
import binascii
sys.path.append(os.getcwd() + '/libs')

from ssd1306 import ssd1306

def getTimeStr():
	return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def getDateStr():
	return datetime.now().strftime("%Y-%m-%d")
def getTimeStr():
	return datetime.now().strftime("%H:%M:%S")

def main():
	oled = ssd1306(port=0)
	oled.fillDisplay(0x5A)

	pagebuf = []
	fd = open('badapple86x64.bin', 'rb')
	#frame = 1
	boolean = True
	while (boolean):
		del pagebuf[:]
		#print "Read %d frame" % frame
		for i in range(8):
			buf = list(bytearray(fd.read(86)))
			if len(buf) < 86:
				boolean = False
				break
                        oled.setLocation(0, i << 3)
			oled.writePage(buf)
			#pagebuf.extend(list(bytearray(buf)))
			#pagebuf.extend([0 for j in range(42)])
		#print binascii.b2a_hex(str(bytearray(pagebuf)))
		#oled.update(pagebuf)
		time.sleep(0.050)
		#frame += 1
	fd.close()
		

	#while(True):
	#	oled.drawLocString8x8(3, 3, getDateStr())
	#	oled.drawLocString8x8(4, 4, getTimeStr())
	#	time.sleep(1)

	#oled.drawLocString8x8(0, 0, "ABCDEFG")
	#oled.drawLocString6x8(0, 1, "ABCDEFG")

if __name__ == "__main__":
	main()
