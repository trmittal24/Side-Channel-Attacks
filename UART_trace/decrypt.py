#!/usr/bin/env python3

import matplotlib.pyplot as pp
import numpy as np
import scipy.io
import sys

try:
	file = sys.argv[1]
	traces = scipy.io.loadmat(file)
except IndexError:
	raise SystemExit('usage:\n\t./processing.py <MAT file containing traces>')


traces = scipy.io.loadmat(file)
t = traces['Trace_1'][:, 0]
data = traces['Trace_1'][:, 1]
#s = traces['Trace_2'][:, 1]

n = len(data)

first = 0
last = 0

for i in range(n):
	if(data[i]<2.5):
		first = i
		break

for i in range(n-1,0,-1):
	if(data[i]<2.5):
		last = i
		break

width = (last - first)/79.0

cipher_text = ""

for i in range(79):

	# print(i,first + width/2 + i*width)	

	if((i%10==0) or (i%10==9) ):
		continue

	if(data[int(first + width/2 + i*width)] > 2.5):
		cipher_text = "1" + cipher_text
	else:
		cipher_text = "0" + cipher_text


print(cipher_text)
print(int(cipher_text,2))

print(file[: -4] == str(int(cipher_text,2)))

pp.figure().canvas.set_window_title('RSA on Arduino')
pp.title('RSA Decryption Power Trace')
# pp.plot(p, 'b-', label = 'power trace', linewidth = 0.8)
pp.plot(data, 'r-', label = 'filtered power trace', linewidth = 0.8)
#pp.plot(s, 'g-', label = 'cycle marker', linewidth = 0.8)
# pp.plot(b, 'y-', label = 'operation marker', linewidth = 0.8)
pp.xlabel('samples')
pp.ylabel('voltage / V')
pp.legend()
pp.grid(True, linewidth = 0.4)
pp.show()
