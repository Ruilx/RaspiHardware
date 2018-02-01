#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
sys.path.append(os.getcwd() + '/libs')

from ssd1306 import ssd1306

def main():
	oled = ssd1306()
	oled.fillDisplay(0x00)

	oled.drawLocString8x8(0, 0, "ABCDEFG")
	oled.drawLocString6x8(0, 1, "ABCDEFG")

if __name__ == "__main__":
	main()
