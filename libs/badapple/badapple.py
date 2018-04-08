# -*- coding: utf-8 -*-

import os, sys, time
import binascii

sys.path.append(os.getcwd() + '../')
from ssd1306 import ssd1306

class badapple:
	def __init__(self, oled, binFile="badapple86x64.bin"):
		if not isinstance(oled, ssd1306):
			assert "Please pass the old handle object." and False
		self.oled = oled
		self.file = binFile

	def __del__():
		if self.binFile:
			self.binFile.close()
