#!/usr/bin/env python3

import os
import sys

# os.system('clear')

def power(M, e, n) :
	C = 1
	while e:
		if e % 2:
			C = C * M % n
		e >>= 1
		M = (n - M * (n - M)) % n
		# print(M, C)
	return C

# p = 56629561; q = 658998563; e = 58765268265842237; d = 26499063470653493;
# n = p * q
# M = 10

# C = power(M, e, n)
# print(C)
C = int(sys.argv[1])
d = int(sys.argv[2])
n = int(sys.argv[3]) * int(sys.argv[4])
M = power(C, d, n)
print(M)
