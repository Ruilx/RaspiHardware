# -*- coding: utf-8 -*-
import os

class unicode16():
	def __init__(self):
		self.file = open(os.path.dirname(os.path.abspath(__file__)) + "/mc16.ptf", "rb")
		assert(self.file, "Cannot open file 'mc16.ptf'")
	
	def __del__(self):
		if self.file:
			self.file.close()

	def getString(self, s):
		if not isinstance(s, unicode):
			if isinstance(s, str):
				s = s.decode("utf-8")
			else:
				assert(False, "s is not unicode string or a UTF-8 string")
		output = []
		for c in s:
			self.file.seek(ord(c) * 32)
			data = [ord(i) for i in self.file.read(32)]
			if sum(data[8:16]) == 0 and sum(data[24:32]) == 0:
				data = data[0:8] + data[16:24]
			output.append(data)
		return output
