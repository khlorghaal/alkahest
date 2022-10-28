#scrap
#used for motif matching
#very optimumnt

import space

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


def rune_rng_a():
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

