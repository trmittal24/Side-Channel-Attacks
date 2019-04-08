#!/usr/bin/env python3

from math import factorial
import matplotlib.pyplot as pp
import numpy as np
import scipy.io
import scipy.signal
import sys

################################################################################

def otsu(gray):
	'''
		Given an array of integers, determine the best threshold to binarise the array.
		https://stackoverflow.com/questions/48213278/implementing-otsu-binarization-from-scratch-python
	'''

	# set up the array for thresholding
	pixel_number = len(gray)
	mean_weigth = 1.0 / pixel_number
	his, bins = np.histogram(gray, np.array(range(min(gray), max(gray))))
	final_thresh = -1 # initialisation
	final_value = -1 # initialisation

	# iterate over all except extreme values
	for t in bins[1 : -1]:

		# calculate inter-class variance
		Wb = np.sum(his[: t]) * mean_weigth
		Wf = np.sum(his[t :]) * mean_weigth
		mub = np.mean(his[: t])
		muf = np.mean(his[t :])
		value = Wb * Wf * (mub - muf) ** 2
		# print('Wb', Wb, 'Wf', Wf)
		# print('t', t, 'value', value)

		# best threshold maximises inter-class variance
		if value > final_value:
			final_thresh = t
			final_value = value

	# print(final_thresh)
	return final_thresh

################################################################################

def savitzky_golay(y, window_size, order, deriv = 0, rate = 1):
	'''
		Savitzky-Golay Filter is a polynomial filter.
		Given a set of consecutive samples (a window), fit a polynomial of the specified degree through them.
		Perform this fitting for all possible windows in the input array.
		Return the polynomial-fitted array as output.
		This implementation seems to be faster than the built-in scipy.signal.savgol_filter function.
		https://stackoverflow.com/questions/29251407/savitzky-golay-filter-plots-wrong-values
	'''

	# check arguments
	try:
		window_size = np.abs(np.int(window_size))
		order = np.abs(np.int(order))
	except ValueError:
		raise ValueError('window_size and order have to be of type int')
	if window_size % 2 != 1 or window_size < 1:
		raise TypeError('window_size size must be a positive odd number')
	if window_size < order + 2:
		raise TypeError('window_size is too small for the polynomials order')

	# set up
	order_range = range(order + 1)
	half_window = (window_size - 1) // 2
	b = np.mat([[k ** i for i in order_range] for k in range(-half_window, half_window + 1)])
	m = np.linalg.pinv(b).A[deriv] * rate ** deriv * factorial(deriv)
	firstvals = y[0] - np.abs(y[1 : half_window + 1][:: -1] - y[0])
	lastvals = y[-1] + np.abs(y[-half_window - 1 : -1][:: -1] - y[-1])
	y = np.concatenate((firstvals, y, lastvals))

	return np.convolve(m[:: -1], y, mode = 'valid')

################################################################################

def get_signatures(file, traces):

	'''
		Load the parameters used to recognise the trace segments.
		The parameters are stored in 'dpa.mat'.
		Analyse the traces using these parameters and predict the number represented by the trace.
	'''

	# load traces
	t = traces['Trace_1'][:, 0] # time
	b = traces['Trace_1'][:, 1] # big marker
	s = traces['Trace_2'][:, 1] # small marker
	p = traces['Trace_3'][:, 1] # power
	f = savitzky_golay(p, 35, 10) # filtered power

	# load parameters using one of the following two lines
	# peak, limit, threshold, first, last = scipy.io.loadmat('dpa.mat')[file][0]
	peak, limit, first, last = [-0.839, 160, 1342, 26885]
	try:
		# peak, limit, first, last = [float(i) for i in sys.argv[2 : 6]]
		first = float(sys.argv[2])
		last = float(sys.argv[3])
	except:
		pass


	# explanation of the parameters
	# 	peak = maximum value - 0.03
	# 	limit = 50
	# 	threshold = Otsu's Thresholding on sequence lengths
	# 	first = point where moving median drops
	# 	last = point where moving median rises

	# use the big marker 'b' to find out where the relevant part of the trace begins and ends
	# the two values printed by this should be approximately the same as 'first' and 'last'
	# make sure to set these two values on line 63 (if you are using it instead of line 62)
	# markers are used only for debugging, not for tracking
	i_prev = 0
	for i in range(len(t)):
		if b[i] < -3:
			if i - i_prev > 1000:
				print(i_prev + 1, i - 1)
				pass
			i_prev = i
			# print(i)
			continue

	# break 'f' into segments such that each segment represents one bit
	# it is broken whenever its value exceeds 'peak'
	start = first
	signatures = [] # list of segments the trace has been broken into
	for i in range(int(first), int(last + 1)): # scipy loads 'first' and 'last' as float

		# detect if 'peak' as been crossed
		if f[i] > peak:

			# if there is one crossing immediately after another, the former should be ignored ...
			if i - start < limit:
				continue

			# ... otherwise, the segment is added to the list
			signatures.append(f[int(start) : i])
			start = i

	# add remaining segment, if any
	if i - start > limit:
		signatures.append(f[start : i])

	# the defining characteristics of the segments are their lengths
	# create an array of their lengths
	# threshold these length values
	# large values: bit is 1
	# small values: bit is 0
	bits = np.array([len(i) for i in signatures])
	threshold = otsu(bits)
	print(peak, limit, threshold, first, last)
	bits[bits <= threshold] = 0
	bits[bits > threshold] = 1
	bits = bits[:: -1] # reverse them because bits are transmitted LSB to MSB

	# represent the above array as a string
	d = ''
	for i in bits:
		d += str(i)
	print('0b{}'.format(d))
	print(int(d, 2)) # the number represented by the trace
	print(str(int(d, 2)) == file[: -5] or str(int(d, 2)) == file[: -4])

################################################################################

if __name__ == '__main__':

	# check arguments
	try:
		file = sys.argv[1]
		traces = scipy.io.loadmat(file)
	except IndexError:
		raise SystemExit('usage:\n\t./demo.py <MAT file containing traces>')

	# if the user provides the two files which give wrong answer
	if file in ['44816101156119797339.mat', '6827596968971589571.mat']:
		print('Unexpected spikes lead to wrong result.')

	# perform analysis of the traces
	get_signatures(file, traces)

	# load traces
	t = traces['Trace_1'][:, 0] # time
	b = traces['Trace_1'][:, 1] # big marker
	s = traces['Trace_2'][:, 1] # small marker
	p = traces['Trace_3'][:, 1] # power
	f = savitzky_golay(p, 35, 10) # filtered power
	# f = scipy.signal.savgol_filter(power, 35, 10) # this seems to be slower than savitzky_golay

	pp.figure().canvas.set_window_title('RSA on Arduino')
	pp.title('RSA Decryption Power Trace')
	# pp.plot(p, 'b-', label = 'power trace', linewidth = 0.8)
	pp.plot(f, 'r-', label = 'filtered power trace', linewidth = 0.8)
	# pp.plot(s, 'g-', label = 'cycle marker', linewidth = 0.8)
	# pp.plot(b, 'y-', label = 'operation marker', linewidth = 0.8)
	pp.xlabel('samples')
	pp.ylabel('voltage / V')
	pp.legend()
	pp.grid(True, linewidth = 0.4)
	pp.show()
