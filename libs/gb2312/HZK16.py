# -*- coding: utf-8 -*-

import sys, struct, binascii
from transpose import transpose16

class HZK16:
	def __init__(self, file="HZK16", length=32):
		self.file = file
		self.length = length
		self._file = open(file, "r")
		if not self._file:
			assert False and "cannot open file"

	def __del__(self):
		if self._file:
			self._file.close()

	def _getOffset(self, firstByte, secondByte):
		if not isinstance(firstByte, (int)):
			if isinstance(firstByte, (str)):
				qh = int(struct.unpack("B", firstByte)[0]) - 0xA1
			else:
				assert False and "firstByte is not an integer or a character"
		else:
			qh = firstByte - 0xA1
		if not isinstance(secondByte, (int)):
                        if isinstance(secondByte, (str)):
                                wh = int(struct.unpack("B", secondByte)[0]) - 0xA1
                        else:
                                assert False and "secondByte is not an integer or a character"
		else:
			wh = secondByte - 0xA1
		return (94 * qh + wh) * 32

	def getSingleChar(self, char):
		if not isinstance(char, (str, unicode)):
			assert False and "getSingleChar not a str or unicode"
		if isinstance(char, unicode):
			c = char.encode("gbk")
		else:
			c = char.decode("utf-8").encode("gb2312")
		offset = self._getOffset(c[0], c[1])
		self._file.seek(offset)
		return self._file.read(self.length)

	def getString(self, string):
		if not isinstance(string, (str, unicode)):
			assert False and "String is not str or unicode"
		l = []
		for c in string.decode("utf-8"):
			a = self.getSingleChar(c)
			#print "c:", c, " a:", binascii.b2a_hex(a)
			l.append(a)
		return l

def printByte(b):
    for i in xrange(8):
        if( b & 0x80 ):
            sys.stdout.write("■")
        else:
            sys.stdout.write("  ")
        b <<= 1

def printChar(c):
	if (not isinstance(c, (list, tuple, str))) or len(c) < 32:
		print "len:", len(c), " type:", type(c)
		assert False and "c must be a list or a tuple and length > 32."
	index = 0
	for b in c:
		printByte(int(struct.unpack("B", b)[0]) & 0xFF)
		if index & 0x01:
			print("")
		index += 1
	pass
def printStr(s, transpose=False):
	if (not isinstance(s, (list, tuple, str))) or len(s[0]) < 32:
		print "len:", len(s[0]), " type:", type(s)
		assert False and "s must be a list or a tuple and [0]length > 32."
	
	if transpose:
		for i in xrange(len(s)):
			c = transpose16([ord(a) for a in s[i]])
			s[i] = c
	else:
		for i in xrange(len(s)):
			s[i] = [a for a in s[i]]
	for i in xrange(16):
		#index = 0
		for c in s:
			#print(c)
			#sys.stdout.write("S[{l}][{w}] ".format(l=index, w=0))
			#sys.stdout.write("S[{l}][{w}] ".format(l=index, w=1))
			printByte(c[2 * i] & 0xFF)
			printByte(c[2 * i + 1] & 0xFF)
			#index += 1
		print("")
	pass
		


if __name__ == '__main__':
	args = sys.argv
	if len(args) < 2:
		assert "Usage: HZK16.py StringOf_GB2312" and False
	a = HZK16()
	dat = a.getString(args[1])
	print(dat)
	dat0 = [ord(i) for i in dat[0]]
	dat2 = transpose16(dat0)
	print(dat2)
	#dat_1 = dat
	#printStr(dat, True)
	#printStr(dat)
