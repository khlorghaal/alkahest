#hyperdimensional numerals via space filling curve

import gl_backend
from com  import *
from math import *
en=enumerate
ra=range

w=8#param
h=8
assert(w>=1)
assert(h>=1)
n=2<<(w*h)

#truthy= '■'
#falsy= '□'
truthy= '▉'
falsy= ' '
truthy= 1
falsy= 0
acc=[]
for g in ra(n):
	def f(x,y):
		i=x+y*w
		b=g&(1<<i)
		return truthy if b else falsy
	rast= [[f(x,y) for x in ra(w)] for y in ra(h)]

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
	yeah=1#all kernels pass
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
					yeah=0
	if yeah:
		gl_backend.blit(rast)
		gl_backend.invoke(8)
		acc+= [rast]

