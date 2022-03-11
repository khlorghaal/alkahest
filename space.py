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
#
class mod:
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
	w:int= 0#movement
	vel_active:bool= 0
	b: body= 0

	def __post_init__(self):
		self.place(ivec2(0,0))
		cursor.insts+=[self]

	def place(self,p):
		if self.b:
			self.b.kill()
		self.b= body(
			p,
			runedict['cursor'],
			-1,
			mod.c)

	def step():
		r=None#dirty
		for c in cursor.insts:
			if c.v!=ivec2(0,0):
				r= True
				d= c.v*(1<<c.w)
				if not c.vel_active:
					c.v*=0#halt
				c.place(c.b.p+d)

		return r
setattr(cursor,'insts',[])
setattr(cursor,'prime',cursor())#because dcls

def thrust(b,d):
	c= cursor.prime
	if c.vel_active:
		c.v+= d if b else -d
	elif b:
		c.v+= d
	else:
		pass
def wset(i):
	def r(b):
		c= cursor.prime
		m=(1<<i)
		if b:
			c.w|= m
		else:
			c.w&=~m
		print('cw %s'%c.w)
	return r


def emplace(name):
	body(cursor.prime.p, runedict[name])

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

def list_bound(l):
	a= ivec2(
		min(l, lambda e:e.x),
		min(l, lambda e:e.y))
	b= ivec2(
		max(l, lambda e:e.x),
		max(l, lambda e:e.y))
	return bound(a,b-a)



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
	

def step():
	#motion
	return cursor.step()