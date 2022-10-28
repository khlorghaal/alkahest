import numpy
from numpy import array

from com  import *
from math import *

Z=5#runes being (1<<5=8)x8 is specified fairly hard

def arrarr_wh(a):
	return (len(a[0]),len(a))

class lib:
	pass
dic={}

class rune:
	_rune_idit=0
	def __init__(self, names, dat):
		if type(dat)==int:
			self.bin= dat
		else:
			assert(type(dat   )==tuple)
			assert(type(dat[0])==tuple)
			assert(arrarr_wh(dat)==(8,8))

			l= lambda x,y: dat[y][x]<<( x+y*8 )
			r= array([([ l(x,y) for x in ra(8)]) for y in ra(8)])
			self.bin= int(numpy.sum(r,dtype='uint64'))&0xFFFFFFFFFFFFFFFF

		self.names= names
		for n in names:
			setattr(lib,n,self)
			dic[n]= self
		dic[self.bin]= self

	def __str__(self):
		s= self.name
		i= self.bin
		for y in ra(8):
			for x in ra(8):
				lum= ((1<<(x+y*8))&i)!=0
				s+= 'X' if lum else '.'
		return s


def strnrm(pile:list[str,rune]):
	ret=[]
	for e in pile:
		if type(e)==rune:
			ret+= [e]
		else:
			assert(type(e)==str)
			for c in e:
				ret+= [dic[c]]
	return ret

bounded= lambda x,y,w,h: x>=0 and y>=0 and x<w and y<h
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
						if bounded(kx+x-1,ky+y-1,w,h):
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
	assert(f.wh==(8,8))
	for g in f.glyphs.values():
		rune(g.names,g.raster)

load_font('./font/lunatic.rmf')

class tests:
	#import atom

	def font():
		import space
		i=0
		l= dic.values()
		l= tuple({e:None for e in l}.keys())#ordered dup eliminate

		W= 12
		ll= len(l)
		assert(ll<W*W*4)
		for y in ra(-W,W):
			for x in ra(-W,W):
				if i>=ll:
					break
				space.body(ivec2(x,y),l[i])
				i+=1

	def descritpions():#of runes
		import space
		i=0
		l= dic.values()
		l= tuple({e:None for e in l}.keys())
		#ordered dup eliminate
		#set quickly bungles ordering

		for y,r in en(l):
			y= 16-y
			x= -8
			x= (y//64)*32
			y= y%64
			space.body(ivec2(x,y),r)
			names= filter(lambda n: len(n)>1,r.names)
			s= ','.join(names)
			for x_,c in en(s):
				space.body(ivec2(x_+x+2,y),dic[c])

			#atom.text(s,ivec2(x+2,y))
			i+=1

	def rune_rng_a():
		import space
		i=256
		for y in ra(-16,8):
			for x in ra(-16,16):
				r= rune('gen_%i'%i,int(1.055**i)&((1<<32)-1))
				space.body(ivec2(x*1,y*1),r)
				i+=1
	def rune_rng_b():
		import space
		i= 256
		for y in ra(-2,2):
			for x in ra(-2,2):
				while gfilter():
					#g= 
					i+= 256
				r= rune('gen_%i%i'%(x,y), g)
				space.body(ivec2(x*1,y*1),r)
				i+=1

