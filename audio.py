#accepts fft input via (TODO)
#TEMPORARY HACK until pyodsp is unfucked

#there is no clear purpose to audio, it is simply obligatory

from numpy import *
from numpy.fft import *
import scipy.fftpack as fftpack
from numpy import complex64
from numpy import *
from scipy.interpolate import splrep,splev
from scipy.signal import resample,resample_poly
from scipy.signal.windows import hann, triang

import threading
import time

from math import  pi as PI
from math import tau as TAU

import sounddevice as sd

#DEBUG= True
DEBUG= False

sdqd= sd.query_devices()
if DEBUG:
	print(sdqd)
#(out,in)
for (i,s) in enumerate(sdqd):
	if 'default' in s:
		sd.default.device= (i,i)
DUPLEX= True
#todo i keep forgetting what the fuck is a duplex



sample_rate = sd.query_devices(sd.default.device if DUPLEX else sd.default.device[0], 'input')['default_samplerate']
def hz_idx(t):
	return (t*sample_count/sample_rate).astype(int)
frame= 0
t0= 0
last_amp= 0# prevents skipping on dropped frames
def audio_callback(indata, outdata, frames, time, status):
	#ASYNC this function is invoked from another thread
	if DEBUG:
		print('______update')
	if status:
		print('STATUS'+str(status))
		print('frames'+str(frames))
	global frame
	global data_p
	global data_pp
	global t0

	#if DEBUG:
		#print('note_array.shape '+note_array.shape)

	out_amp= outdata[:,0].view()
	out_frq= zeros(frames//2+1,dtype=complex64)

	t1= t0+float(frames)
	rate= sample_rate
	if DEBUG:
		print('interval '+str(t0-t1))

	out_frq[:]= piano(rate,len(out_frq))
	
	#lowpass
	_lk= 200#half-frequency, reciprocal
	out_frq*= square(_lk/arange(_lk,_lk+out_frq.size)) # 1 -> lim 0
	#out_amp[:]= irfft(out_frq, n=len(out_amp))
	out_amp[:]= irfft(out_frq*1j, n=len(out_amp))
		# *1j does cosine->sine, to taper ends and mostly elim need for windowing
		#todo n should not need specified

	t0= t1
	frame+= frames


from queue import Queue
fifo= Queue()
_lock=threading.Lock()
def note(b,idx):
	_lock.acquire()
	fifo.put((b,idx))
	_lock.release()
note_state= zeros(256)

def piano(rate,count):
	_lock.acquire()
	for e in fifo.queue:
		note_state[e[1]]=e[0]
	fifo.queue.clear()
	_lock.release()

	ofreq= zeros(count)
	notes= note_state.copy()
	#notes[0]=1 sanity test
	notes[:size(notes)]+= notes
	notes*= arange(1,1+notes.size)
	notes= notes*2.
	notes= notes.astype('int')
	notes= minimum(notes,ofreq.size-1)#clamp index
	ofreq[notes]= 1
	#normalize
	s= sum(ofreq)
	if absolute(s)>0.:
		ofreq*= ofreq.size/s
	return ofreq

def start():
	def f():
		try:
			with sd.Stream(
				samplerate=sample_rate,
				#blocksize=fftsize,
				blocksize=2048,
				#dtype=None, latency=None,
				clip_off=True,
				dither_off= True,
				##never_drop_input= True,
				channels=1,#mono input and output
				#latency='high',
				callback= audio_callback):
					while 1:
						threading.Event().wait()
						print('no')
		except Exception as e: 
			print("\nEXCEPT")
		    #always check if devices are configured via sd.default.device
			raise e
	threading.Thread(target=f,daemon=1).start()
