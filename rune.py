import numpy
from numpy import array
#import ioplex

from com  import *
from math import *
en=enumerate
ra=range

Z=5#runes being (1<<5=8)x8 is specified fairly hard

def arrarr_wh(a):
	return (len(a[0]),len(a))

class rune:
	_idit=0
	def __init__(self, name, dat):
		if type(dat)==int:
			self.bin= dat
		else:
			assert(type(dat   )==tuple)
			assert(type(dat[0])==tuple)
			assert(arrarr_wh(dat)==(8,8))

			l= lambda x,y: dat[y][x]<<( x+y*8 )
			r= array([([ l(x,y) for x in ra(8)]) for y in ra(8)])
			self.bin= int(numpy.sum(r,dtype='uint64'))&0xFFFFFFFFFFFFFFFF

		self.name= name
		rune.lib[name]=self
	lib={}

	def __str__(self):
		s= self.name
		i= self.bin
		for y in ra(8):
			for x in ra(8):
				lum= ((1<<(x+y*8))&i)!=0
				s+= 'X' if lum else '.'
		return s

bound= lambda x,y,w,h: x>=0 and y>=0 and x<w and y<h
def gfilter(rast):
	#rejection cases
	krn=[[
	[0,1],
	[1,0]
	],[
	[1,0],
	[0,1]
	],[
	[1,1],
	[1,1]
	],[
	[0,0,0],
	[0,1,0],
	[0,0,0]
	]]
	h= len(rast)
	w= len(rast[0])
	for y,l in en(rast):
		for x,rv in en(l):
			for k in krn:
				kres=1#kernel result per pixel
				#reject if any kernel passes on any pixel
				for ky,kl in en(k):
					for kx,kv in en(kl):
						if bound(kx+x-1,ky+y-1,w,h):
							rv= rast[y][x]
						else:
							rv= 0
						kres&= kv==rv#every
				if kres:
					return 0
	return 1

def combine(w=4,h=4, count=None):
	assert(w>=1)
	assert(h>=1)
	n=2<<(w*h)

	acc=[]
	def f(x,y):
		i=x+y*w
		b=g&(1<<i)
		return b

	count_=0
	for g in ra(n):
		rast= [[f(x,y) for x in ra(w)] for y in ra(h)]
		if gfilter(rast):
			acc+=[rast]
			count_+= 1
			if count_>count:
				break
			#print(join2d(rast)+'\n')
	return acc


def load_font(file):
	import font
	from font import rmf
	f= rmf.load(file)

	for c,g in f.glyphs.items():
		name= c
		rast= g.raster
		#border
		rast= [[*l]+[0] for l in rast]+[[0]*8]
		rast= tuple(tuple(l) for l in rast)
		rune(name,rast)

rune('blank' ,0)
rune('solid' ,0xFFFFFFFFFFFFFFFF)
rune('border',0xFF818181818181FF)
load_font('./font/lunatic.rmf')

def text(s,p):
	import space
	for y,l in en(s.split('\n')):
		x=0
		for c in l:
			if c=='\t':
				x+=4
				continue
			if c!=' ':
				space.body(ivec2(x+p.x,y+p.y),rune.lib[c])
			x+=1

def tests():
	import space
	#rand
	if 0:
		i=256
		for y in ra(-16,8):
			for x in ra(-16,16):
				r= rune('gen_%i'%i,int(1.055**i)&((1<<32)-1))
				space.body(ivec2(x*1,y*1),r)
				i+=1

	if 0:
		i= 256
		for y in ra(-2,2):
			for x in ra(-2,2):
				while gfilter():
					#g= 
					i+= 256
				r= rune('gen_%i%i'%(x,y), g)
				space.body(ivec2(x*1,y*1),r)
				i+=1

	#font
	if 0:
		i=0
		l= tuple(rune.lib.values())
		W= 8
		for y in ra(-W,W):
			for x in ra(-W,W):
				if i>=len(l):
					break
				space.body(ivec2(x,y),l[i])
				i+=1

	#strings
	if 1:
		s= '''
		def load_font(file):
	import font
	from font import rmf
	f= rmf.load(file)

	for c,g in f.glyphs.items():
		name= c
		rast= g.raster
		#border
		rast= [[*l]+[0] for l in rast]+[[0]*8]
		rast= tuple(tuple(l) for l in rast)
		rune(name,rast)

rune('blank' ,0)
rune('solid' ,0xFFFFFFFFFFFFFFFF)
rune('border',0xFF818181818181FF)
load_font('./font/lunatic.rmf')

def text(s,p):
	import space
	for y,l in en(s.split('\n')):
		x=0
		for c in l:
			if c=='\t':
				x+=4
				continue
			if c!=' ':
				space.body(ivec2(x+p.x,y+p.y),rune.lib[c])
			x+=1

def tests():
	import space
	#rand
	if 0:
		i=256
		for y in ra(-16,8):
			for x in ra(-16,16):
				r= rune('gen_%i'%i,int(1.055**i)&((1<<32)-1))
				space.body(ivec2(x*1,y*1),r)
				i+=1

	if 0:
		i= 256
		for y in ra(-2,2):
			for x in ra(-2,2):
				while gfilter():
					#g= 
					i+= 256
				r= rune('gen_%i%i'%(x,y), g)
				space.body(ivec2(x*1,y*1),r)
				i+=1

	#font
	if 0:
		i=0
		l= tuple(rune.lib.values())
		W= 8
		for y in ra(-W,W):
			for x in ra(-W,W):
				if i>=len(l):
					break
				space.body(ivec2(x,y),l[i])
				i+=1

	#strings
	if 1:
		s= \'\'\'\'\'\'
		text(s,ivec2(-16,16))
		'''
		text(s,ivec2(-16,64))

