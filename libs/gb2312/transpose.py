# -*- coding: utf-8 -*-

def transpose8(A, m, B, n):
	assert isinstance(A, (list)), "A must be a list."
	assert isinstance(B, (list)), "B must be a list."
	assert len(A) >= (8 * m), "List A must be 8 times argument 'm'. length of A: " + str(len(A))
	assert len(B) >= (8 * n), "List B must be 8 times argument 'n'. length of B: " + str(len(B))

	x = (A[0]     << 24) | (A[m]     << 16) | (A[m * 2] << 8) | (A[m * 3])
	y = (A[m * 4] << 24) | (A[m * 5] << 16) | (A[m * 6] << 8) | (A[m * 7])

	t = (x ^ (x >>  7)) & 0x00AA00AA
	x = x ^ t ^ (t <<  7)
	t = (y ^ (y >>  7)) & 0x00AA00AA
	y = y ^ t ^ (t <<  7)

	t = (x ^ (x >> 14)) & 0x0000CCCC
	x = x ^ t ^ (t << 14)
	t = (y ^ (y >> 14)) & 0x0000CCCC
	y = y ^ t ^ (t << 14)

	t = (x & 0xF0F0F0F0) | ((y >> 4) & 0x0F0F0F0F)
	y = ((x << 4) & 0xF0F0F0F0) | (y & 0x0F0F0F0F)
	x = t

	B[0] = (x >> 24) & 0x000000FF
	B[n] = (x >> 16) & 0x000000FF
	B[2 * n] = (x >> 8) & 0x000000FF
	B[3 * n] = x & 0x000000FF
	B[4 * n] = (y >> 24) & 0x000000FF
	B[5 * n] = (y >> 16) & 0x000000FF
	B[6 * n] = (y >> 8) & 0x000000FF
	B[7 * n] = y & 0x000000FF

	return B

def transpose16(A):
	assert isinstance(A, list), "A is not a list."
	assert len(A) >= 32, "List A length must be 32. Length:" + str(len(A))
	_1 = [A[0], A[2], A[4], A[6], A[8], A[10], A[12], A[14]]
	_2 = [A[1], A[3], A[5], A[7], A[9], A[11], A[13], A[15]]
	_3 = [A[16], A[18], A[20], A[22], A[24], A[26], A[28], A[30]]
	_4 = [A[17], A[19], A[21], A[23], A[25], A[27], A[29], A[31]]
	__1 = [0x00] * 8
	__2 = [0x00] * 8
	__3 = [0x00] * 8
	__4 = [0x00] * 8
	transpose8(_1, 1, __1, 1)
	transpose8(_2, 1, __2, 1)
	transpose8(_3, 1, __3, 1)
	transpose8(_4, 1, __4, 1)
	__1 = reverse8(__1)
	__1.extend(reverse8(__2))
	__1.extend(reverse8(__3))
	__1.extend(reverse8(__4))
	return __1

def reverse8(A):
	if isinstance(A, list):
		B = []
		for a in A:
			B.append(0xFF & (((a * 0x0802 & 0x22110) | (a * 0x8020 & 0x88440)) * 0x10101 >> 16))
		return B
	else:
		return 0xFF & (((A * 0x0802 & 0x22110) | (A * 0x8020 & 0x88440)) * 0x10101 >> 16)

def main():
	A = [0b00010000, 0b00100100, 0b01000010, 0b11111111, 0b00000001, 0b00000000, 0b01111110, 0b01000010]
	B = [0x00] * 8

	transpose8(A, 1, B, 1)

	print(A)
	print(B)
	
if __name__ == '__main__':
	main()

