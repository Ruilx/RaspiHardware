# -*- coding: utf-8 -*-

import smbus
from time import *
from consts import *
from ascii6x8 import ascii6x8
from ascii8x8 import ascii8x8
from unicode16 import unicode16

class ssd1306(object):
	def __init__(self, address = 0x3C, port = 0):
		self.address = address
		self.port = port
		self.maxCol = 128
		self.maxRow = 64
		self.maxPage = 8

		self.currentCol = 0
		self.currentPage = 0

		self.bus = smbus.SMBus(port)
		self.uni = None
		self.init()

	def sendCmd(self, cmd):
		self.bus.write_byte_data(self.address, 0x00, cmd)

	def sendData(self, data):
		if not isinstance(data, list):
			self.bus.write_i2c_block_data(self.address, 0x40, data)
		else:
			if len(data) < 32:
				self.bus.write_i2c_block_data(self.address, 0x40, data)
			else:
				i = len(data) / 32
				for j in range(i):
					self.bus.write_i2c_block_data(self.address, 0x40, data[j * 32: (j + 1) * 32])
				if len(data) % 32 != 0:
					self.bus.write_i2c_block_data(self.address, 0x40, data[i * 32:])

	def fillDisplay(self, unit):
		unit = unit & 0xFF
		for i in range(self.maxPage):
			self.sendCmd(0xB0 | i)
			self.sendCmd(0x00)
			self.sendCmd(0x10)
			self.sendData([unit for i in range(128)])

	def fillDis(self, unit):
		self.fillDisplay(unit)

	def clear(self):
		self.fillDisplay(0x00)

	def init(self):
		self.sendCmd(SET_DISPLAY_ON)
		self.sendCmd(SET_MEMORY_ADDRESSING_MODE)
		self.sendCmd(0x10)
		self.sendCmd(SET_PAGE_START_ADDRESS_FOR_PAGE_ADDRESSING_MODE(0))
		self.sendCmd(SET_COM_OUTPUT_SCAN_DIRECTION_INVERSE)
		self.sendCmd(SET_LOWER_COLUMN_START_ADDRESS_FOR_PAGE_ADDRESSING_MODE(0))
		self.sendCmd(SET_HIGHER_COLUMN_START_ADDRESS_FOR_PAGE_ADDRESSING_MODE(0))
		self.sendCmd(SET_DISPLAY_START_LINE(0))
		self.sendCmd(SET_CONTRAST_CONTROL)
		self.sendCmd(0x7F)
		self.sendCmd(SET_SEGMENT_RE_MAP_127)
		self.sendCmd(SET_DIRECT_DISPLAY)
		self.sendCmd(SET_MULTIPLEX_RATIO)
		self.sendCmd(0x3F)
		self.sendCmd(SET_ENTIRE_DISPLAY_NORMAL)
		self.sendCmd(SET_DISPLAY_OFFSET)
		self.sendCmd(0x00)
		self.sendCmd(SET_DISPLAY_CLOCK_DIVIDE_RATIO_OSCILLATOR_FREQUENCY)
		self.sendCmd(0xF0)
		self.sendCmd(SET_PRE_CHARGE_PERIOD)
		self.sendCmd(0x22)
		self.sendCmd(SET_COM_PINS_HARDWARE_CONFIGURATION)
		self.sendCmd(0x12)
		self.sendCmd(SET_VCOMH_DESELECT_LEVEL)
		self.sendCmd(0x20)
		self.sendCmd(0x8D)
		self.sendCmd(0x14)
		self.sendCmd(SET_DISPLAY_ON)

	def setContrast(self, value = 0x7F):
		self.sendCmd(SET_CONTRAST_CONTROL)
		self.sendCmd(value)

	def setEntireDisplayOn(self):
		self.sendCmd(SET_ENTIRE_DISPLAY_ON)

	def setEntireDisplayNormal(self):
		self.sendCmd(SET_ENTIRE_DISPLAY_NORMAL)

	def setDisplayInverse(self, inverse):
		self.sendCmd(SET_INVERSE_DISPLAY if inverse else SET_DIRECT_DISPLAY)

	def setDisplayEnable(self, enable):
		self.sendCmd(SET_DISPLAY_ON if enable else SET_DISPLAY_OFF)

	def setContinuousRightHorizonalScroll(self, startPage, frameFreq, endPage):
		if endPage < startPage:
			return
		self.sendCmd(SET_CONTINUOUS_RIGHT_HORIZONAL_SCROLL)
		self.sendCmd(0x00)
		self.sendCmd(startPage & 0x07)
		self.sendCmd(frameFreq & 0x07)
		self.sendCmd(endPage & 0x07)
		self.sendCmd(0x00)
		self.sendCmd(0xFF)

	def setContinuousLeftHorizonalScroll(self, startPage, frameFreq, endPage):
		if endPage < startPage:
			return
		self.sendCmd(SET_CONTINUOUS_LEFT_HORIZONAL_SCROLL)
		self.sendCmd(0x00)
		self.sendCmd(startPage & 0x07)
		self.sendCmd(frameFreq & 0x07)
		self.sendCmd(endPage & 0x07)
		self.sendCmd(0x00)
		self.sendCmd(0xFF)

	def setContinuousVerticalAndRightHorizonalScroll(self, startPage, frameFreq, endPage, verticalScrollingOffset):
		if endPage < startPage:
			return
		self.sendCmd(SET_CONTINUOUS_VERTICAL_AND_RIGHT_HORIZONAL_SCROLL)
		self.sendCmd(0x00)
		self.sendCmd(startPage & 0x07)
		self.sendCmd(frameFreq & 0x07)
		self.sendCmd(endPage & 0x07)
		self.sendCmd(verticalScrollingOffset & 0x3F)

	def setContinuousVerticalAndLeftHorizonalScroll(self, startPage, frameFreq, endPage, verticalScrollingOffset):
		if endPage < startPage:
			return
		self.sendCmd(SET_CONTINUOUS_VERTICAL_AND_LEFT_HORIZONAL_SCROLL)
		self.sendCmd(0x00)
		self.sendCmd(startPage & 0x07)
		self.sendCmd(frameFreq & 0x07)
		self.sendCmd(endPage & 0x07)
		self.sendCmd(verticalScrollingOffset & 0x3F)

	def setDeacrivateScroll(self):
		self.sendCmd(SET_CONTINUOUS_SCROLL_STOP)

	def setActivateScroll(self):
		self.sendCmd(SET_CONTINUOUS_SCROLL_START)

	def setVerticalScrollArea(self, startRow, lengthRow):
		self.sendCmd(SET_VERTICAL_SCROLL_AREA)
		self.sendCmd(startRow & 0x3F)
		self.sendCmd(lengthRow & 0x7F)

	def setLowerColumnStartAddressForPageAddressingMode(self, lowerStartAddress):
		self.sendCmd(SET_LOWER_COLUMN_START_ADDRESS_FOR_PAGE_ADDRESSING_MODE(lowerStartAddress & 0x0F))

	def setHigherColumnStartAddressForPageAddressingMode(self, higherStartAddress):
		self.sendCmd(SET_HIGHER_COLUMN_START_ADDRESS_FOR_PAGE_ADDRESSING_MODE(higherStartAddress & 0x0F))

	def setColumnStartAddressForPageAddressingMode(self, startAddress):
		self.currentCol = startAddress
		self.setLowerColumnStartAddressForPageAddressingMode(startAddress & 0x0F)
		self.setHigherColumnStartAddressForPageAddressingMode(startAddress >> 4)

	def setMemoryAddressingMode(self, mode):
		self.sendCmd(SET_MEMORY_ADDRESSING_MODE)
		self.sendCmd(mode)

	def setColumnAddress(self, startColumnAddress, endColumnAddress):
		self.sendCmd(SET_COLUMN_ADDRESS)
		self.sendCmd(startColumnAddress)
		self.sendCmd(endColumnAddress)

	def setPageStartAddressForPageAddressingMode(self, pageStartAddress):
		self.currentPage = pageStartAddress
		self.sendCmd(SET_PAGE_START_ADDRESS_FOR_PAGE_ADDRESSING_MODE(pageStartAddress))

	def setDisplayStartLine(self, line):
		self.sendCmd(SET_DISPLAY_START_LINE)

	def setSegmentReMap(self, e):
		if e:
			self.sendCmd(SET_SEGMENT_RE_MAP_127)
		else:
			self.sendCmd(SET_SEGMENT_RE_MAP_0)

	def setMultiplexRatio(self, ratio):
		if ratio <= 14:
			return
		self.sendCmd(SET_MULTIPLEX_RATIO)
		self.sendCmd(ratio)

	def setComOutputScanDirection(self, e):
		if e:
			self.sendCmd(SET_COM_OUTPUT_SCAN_DIRECTION_INVERSE)
		else:
			self.sendCmd(SET_COM_OUTPUT_SCAN_DIRECTION_DIRECT)

	def setDisplayOffset(self, offset):
		self.sendCmd(SET_DISPLAY_OFFSET)
		self.sendCmd(offset)

	def setComPinsHardwareConfiguration(self, conf):
		self.sendCmd(SET_COM_PINS_HARDWARE_CONFIGURATION)
		self.sendCmd(conf)

	def setDisplayClockDivideRatioOscillatorFrequency(self, divideRatioOfTheDisplayClocks, oscillatorFrequency):
		self.sendCmd(SET_DISPLAY_CLOCK_DIVIDE_RATIO_OSCILLATOR_FREQUENCY)
		self.sendCmd((oscillatorFrequency << 4) | (divideRatioOfTheDisplayClocks & 0x0F))

	def setPrechargePeriod(self, period1, period2):
		if (period1 == 0 or period2 == 0):
		   return
		self.sendCmd(SET_PRE_CHARGE_PERIOD)
		self.sendCmd((period2 << 4) | (period1 & 0x0F))

	def setVcomhDeselectLevel(self, level):
		self.sendCmd(SET_VCOMH_DESELECT_LEVEL)
		self.sendCmd(level)

	def nop(self):
		self.sendCmd(NOP)

	def writePage(self, data):
		if not isinstance(data, list):
			return
		self.sendData(data)

		pages = int(len(data) / self.maxCol)
		self.currentCol += len(data) % self.maxCol
		if(self.currentCol >= self.maxCol):
			self.currentPage += 1
			self.currentCol -= self.maxCol
		self.currentPage += pages % self.maxPage

	def update(self, buf):
		if not isinstance(buf, list):
			s = []
			s.extend([(buf & 0xFF) for i in range(1024)])
			self.setMemoryAddressingMode(HorizontalAddressingMode)
			self.writePage(s)
		else:
			if len(buf) < 1024:
				buf.extend([0x00 for i in range(1024 - len(buf))])
			self.setMemoryAddressingMode(HorizontalAddressingMode)
			self.writePage(buf)

	def updatePage(self, col, page, buf):
		if not isinstance(buf, list):
			return
		#if self.maxCol <= col + len(buf):
		#    buf = buf[:(maxCol - col)]
		self.setPageStartAddressForPageAddressingMode(page)
		self.setColumnStartAddressForPageAddressingMode(col)
		self.setMemoryAddressingMode(HorizontalAddressingMode)
		self.writePage(buf)

	def __set8x8Location(self, col, row):
		if (col >= 16 or row >= 8):
			col = 0
			row = 0
		xStart = col << 3
		self.setPageStartAddressForPageAddressingMode(row)
		self.setColumnStartAddressForPageAddressingMode(xStart)

	def __set6x8Location(self, col, row):
		if (col >= 21 or row >= 8):
			col = 0
			row = 0
		xStart = (col << 2) + (col << 1)
		self.setPageStartAddressForPageAddressingMode(row)
		self.setColumnStartAddressForPageAddressingMode(xStart)

	def setLocation(self, col, row):
		# 如果设置的地址就是当前显示内存指针的地址, 则退出不设置(因为一样)
		if (col == self.currentCol and (row >> 3) == self.currentPage):
			return
		if col >= self.maxCol or row >= self.maxRow:
			return
		self.setPageStartAddressForPageAddressingMode(row >> 3)
		self.setColumnStartAddressForPageAddressingMode(col)

	def setPageColumn(self, col, page):
		assert col < 127, "Column is out of range."
		assert page < 7, "Page is out of range."
		self.setLocation(col, page * 8)

	def __drawString8x8(self, string, inverse = False):
		if not isinstance(string, str):
			return
		count = 0
		for char in string:
			charArray = ascii8x8[ord(char) - 32]
			if inverse:
				b = [(~i & 0xFF) for i in charArray]
				self.writePage(b)
			else:
				self.writePage(charArray)
			count += 1
			if count >= 16:
				break

	def __drawString6x8(self, string, inverse = False):
		if not isinstance(string, str):
			return
		count = 0
		for char in string:
			charArray = ascii6x8[ord(char)]
			charArray = charArray[:6]
			if inverse:
				b = [(~i & 0xFF) for i in charArray]
				self.writePage(b)
			else:
				self.writePage(charArray)
			count += 1
			if count >= 21:
				break

	def __drawUnicodeAbove(self, data, inverse = False):
		if not isinstance(data, (tuple, list)):
			return
		for d in data:
			if (not isinstance(d, (tuple, list))):
				return
			if inverse:
				b = [(~i & 0xFF) for i in d[:(len(d) >> 1)]]
				self.writePage(b)
			else:
				self.writePage(d[:(len(d) >> 1)])

	def __drawUnicodeBottom(self, data, inverse = False):
		if not isinstance(data, (tuple, list)):
			return
		for d in data:
			if (not isinstance(d, (tuple, list))):
				return
			if inverse:
				b = [(~i & 0xFF) for i in d[(len(d) >> 1):]]
				self.writePage(b)
			else:
				self.writePage(d[len(d) >> 1:])

	def drawLocString8x8(self, col, page, string, inverse = False):
		self.__set8x8Location(col, page)
		self.__drawString8x8(string, inverse)

	def drawLocString6x8(self, col, page, string, inverse = False):
		self.__set6x8Location(col, page)
		self.__drawString6x8(string, inverse)

	def drawLocUnicodeString16x16(self, col, page, string, inverse = False):
		if not isinstance(string, (str, unicode)):
			return;
		if self.uni == None:
			self.uni = unicode16()
		listlist = self.uni.getString(string)
		self.setPageColumn(col, page)
		self.__drawUnicodeAbove(listlist, inverse)
		if page < 7:
			self.setPageColumn(col, page + 1)
			self.__drawUnicodeBottom(listlist, inverse)
		

