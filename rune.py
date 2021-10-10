import numpy
#import ioplex

from com  import *
from math import *
en=enumerate
ra=range

def arrarr_wh(a):
	return (len(a[0]),len(a))

class rune:
	table={}
	_idit=0
	def __init__(self, name, arrarr):
		assert(arrarr_wh(arrarr)==(8,8))

		assert(name not in table)
		table[name]=self

		self.arrarr= arrarr.copy()
		self.np= numpy.array(arrarr, dtype='uint8')
		self.id= _idit
		_idit+=1

		self.rune= [['FIXME' for x,b in r] for y,r in en()]



def combine():
	w=4#param
	h=4
	assert(w>=1)
	assert(h>=1)
	n=2<<(w*h)

	#truthy= '■'
	#falsy= '□'
	truthy= '▉'
	falsy= ' '
	#truthy= 1
	#falsy= 0
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
								kres&= kv==rv
						if kres:
							return 0
			return 1
		if a():
			pass
			#print(join2d(rast)+'\n')
			#ioplex.body(rast)
			#gl_backend.blit(rast)
			#gl_backend.invoke()
			#acc+= [rast]

