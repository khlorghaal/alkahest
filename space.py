from com import *
from rune import dic as runedict
from rune import rune

grid= {}

#bitmaskfield (very fucky)
#mod bits
#max=32
#Sb e? (name|enum) (//(comment))?
#S= symbol
#b= number of bits int of [0,max]
#m= type is mutex-enum
#	a mutex enum is a set of bools
#	where only one may be selected
#	count be 1<<b where b>0
#if (!m): is an int
#
#a2 e bland,active,inactive,spicey
#h1 highlight //because whatever
#v1 verboten //ree
#p1 primary //only one of each type exists
#c1 cursor //bracket-ish-s indicating cursor present
#w2 e ortho,parallax,perspective,skew //projection
#axp3 //arity-count per side [0,8]
#axn3 //where 0u is void-ary 
#ayp3 //      4u is 16-ary
#ayn3 
#rot2 rotation, cardinal
#
class mod:
	none= 0b00000000000000000000000000000000
	a=    0b11000000000000000000000000000000
	h=    0b00100000000000000000000000000000
	v=    0b00010000000000000000000000000000
	p=    0b00001000000000000000000000000000
	c=    0b00000100000000000000000000000000
	w=    0b00000011000000000000000000000000
	w0=   0b00000001000000000000000000000000
	axp = 0b00000000111000000000000000000000
	axp0= 0b00000000001000000000000000000000
	axn = 0b00000000000111000000000000000000
	axn0= 0b00000000000001000000000000000000
	ayp = 0b00000000000000111000000000000000
	ayp0= 0b00000000000000001000000000000000
	ayn = 0b00000000000000000111000000000000
	ayn0= 0b00000000000000000001000000000000
	rot = 0b00000000000000000000110000000000
	rot0= 0b00000000000000000000010000000000
	smol= 0b00000000000000000000001000000000
	#    0b00000000000000000000000000000000


@immut
class body:
	p: ivec2
	rune: rune
	z: int=0
	mod: int=0

	h= lambda s:(s.p,s.z)

	def __post_init__(self):
		h= self.h()
		o= grid.pop(h,None)
		if o==runedict['vescicle']:
			pass
			#todo dtor lol
			#for b in vescicle[self.p].bound:
			#	kill(b)
		grid[h]= self


	def kill(self):
		grid.pop(self.h(),None)

origin= body(ivec2(0,0),runedict['empty'])

@dcls
class cursor:
	v:ivec2= ivec2(0,0)
	vel_active:bool= 0
	b: body= 0
	z= 0#zoom, unrelated to body-z

	def __post_init__(self):
		self.place(ivec2(0,0))
		cursor.insts+=[self]

	def zoom(self, d):
		z=self.z
		z+= d
		z= max(z,0)
		z= min(z,4)
		self.z=z

	def place(self,p):
		if self.b:
			self.b.kill()
		self.b= body(
			p,
			runedict['cursor'],
			1,
			mod.c)

	def step():
		r=None#dirty
		for c in cursor.insts:
			if c.v!=ivec2(0,0):
				r= True
				d= c.v
				c.v*=0#halt
				c.place(c.b.p+d)
		return r

setattr(cursor,'insts',[])
setattr(cursor,'prime',cursor())#because dcls

def thrust(d:ivec2):
	cursor.prime.v+= d


def emplace(name):
	body(cursor.prime.b.p, runedict[name])

snake=   lambda p,w:   int(p.y*w+p.x)
snakent= lambda i,w: ivec2(  i%w,i/w)


@dcls
class bound:
	org: ivec2
	dim: ivec2
	def __iter__(self):#snake
		x0= self.org.x
		y0= self.org.y
		x1= self.org.x+self.dim.x
		y1= self.org.y+self.dim.y
		return (ivec2(x,y) for y in range(y0,y1) for x in (range(x0,x1)))
	def within(self,p:ivec2):
		x0= self.org.x
		y0= self.org.y
		x1= x0+self.dim.x
		y1= y0+self.dim.y
		return x>=x0 and y>=y0 and x<x1 and y<y1

	def compute(bodies:list[body]):
		bp= [b.p for b in bodies]
		x0= min((i.x for i in bp))
		y0= min((i.y for i in bp))
		x1= max((i.x for i in bp))
		y1= max((i.y for i in bp))
		w,h=(
			x1-x0+1,
			y1-y0+1)
		return bound(ivec2(x0,y0),ivec2(w,h))


def aktivat(de):
	b= grid.get(cursor.prime.b.h())
	b= b==focus() or b==None
	focus( b if b else de )

def tests():
	#z
	if 0:
		for i in range(-4,4):
			for p in bound(ivec2(0,-4),ivec2(1,8)):
				body(p,runedict['coplanrect'],i,0)

def load():
	from numpy import array
	from numpy import zeros
	import png
	try:
		img= png.Reader('default.grid.png').read()
	except:
		print('gridfile not found')
		return
	(w,h)= img[:2]
	rast= array(list(img[2]))

	for y,l in en(rast):
		px=[(int(b0)    )|\
			(int(b1)<<16)|\
			(int(b2)<<32)|\
			(int(b3)<<48)
			for b0,b1,b2,b3 in 
			zip(l[0::4],
				l[1::4],
				l[2::4],
				l[3::4],)]
		for x,b in en(px):
			if b!=0:
				if b in runedict:
					body(ivec2(x,y),runedict[b])
				else:
					print('warn, rune not in dict 0x%16x'%b)

def save():
	from numpy import array
	from numpy import zeros
	from numpy import uint16
	import png

	Z= 0 #z 0 is only nonvolatile layer saved
	bnd= bound.compute(
		list(filter(
			lambda b: b.z==Z,
			grid.values())))
	(w,h)= (bnd.dim.x,bnd.dim.y)
	#print(b)
	if w==0 or h==0:
		return
	rast= zeros((w,h),dtype=uint64)
	for b in grid.values():
		if b.z!=Z:
			continue
		i= b.rune.bin
		#print('{0:064b}'.format(i))
		p= b.p
		o= bnd.org
		rast[
			p.x-o.x,
			p.y-o.y
			]= i

	rast= array((
		(rast    )&0xffff,
		(rast>>16)&0xffff,
		(rast>>32)&0xffff,
		(rast>>48)&0xffff
		),dtype=uint16).transpose((2,1,0))
	#print(rast)
	img= png.Writer(
		w,h,
		bitdepth=16,
		greyscale=False,
		alpha= True,
		compression=5
		)
	img.write_array( open('default.grid.png','wb'), rast.flatten() )

def step():
	#motion
	return cursor.step()