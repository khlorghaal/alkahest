import numpy
from numpy import array
#import ioplex

from com  import *
from math import *
en=enumerate
ra=range

Z=5#runes being 8x8 is specified fairly hard

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

		lib= rune.lib
		assert(name not in lib.__dict__)
		setattr(lib,name,self)

	class lib:
		pass

for g in [
		('solid' ,lambda _: 1),
		('blank' ,lambda _: 0),
		('border',lambda p: p.x==0 or p.x==8 or p.y==0 or p.y==8),
]:

	r= tuple( tuple((g[1](ivec2(x,y)) for x in ra(8) )) for y in ra(8))
	rune( g[0],r)


def combine(w=4,h=4,text=False):
	assert(w>=1)
	assert(h>=1)
	n=2<<(w*h)

	if text:
		#truthy= '■'
		#falsy= '□'
		truthy= '▉'
		falsy= ' '
	else:
		truthy= 1
		falsy= 0

	acc=[]
	def f(x,y):
		i=x+y*w
		b=g&(1<<i)
		return truthy if b else falsy
	def t(x,y):
		#boundary condition via 0 padding
		if x<0 or y<0 or x>=w or y>=h:
			return falsy
		return rast[y][x]

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
	for g in ra(n):
		rast= [[f(x,y) for x in ra(w)] for y in ra(h)]

		def a():
			for y,l in en(rast):
				for x,rv in en(l):
					for k in krn:
						kres=1#kernel result per pixel
						#reject if any kernel passes on any pixel
						for ky,kl in en(k):
							for kx,kv in en(kl):
								kv= truthy if kv else falsy
								rv= t(kx+x-1,ky+y-1)
								kres&= kv==rv#every
						if kres:
							return 0
			return 1
		if a():
			print(join2d(rast)+'\n')

