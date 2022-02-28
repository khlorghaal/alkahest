from com import *
from rune import dic as runedict
from rune import rune

grid= {}

@immut
class body:
	p: ivec2
	rune: rune
	z: int= 0
	mod: int=0#misc bits, can be activity, arity, etc
	def __post_init__(self):
		o= grid.pop(self.p,None)
		if o==runedict['vescicle']:
			pass#todo dtor
		grid[self.p]= self

	def kill(self):
		grid.pop(self.p,None)

#origin= body(ivec2(0,0),runedict['empty'])

#cursor is not a body, as it overlaps spaces
@dcls
class cursor:
	p:ivec2
	v:ivec2= ivec2(0,0)
	z:int= 0
	w:int= 0#movement
	mod: int=0
	rune: rune= runedict['cursor']
	vel_active:bool= 0

	def __post_init__(self):
		cursor.insts+=[self]

	def thrust(self,b,d):
		if self.vel_active:
			self.v= d if b else -d
		elif b:
			self.p+= d*(1<<self.w)
	def step():
		r=None
		for c in cursor.insts:
			if c.vel_active:
				r=True
				raise#fixme
				c.p+= c.v*(1<<z)
		return r
setattr(cursor,'insts',[])
setattr(cursor,'prime',cursor(ivec2(0,0)))#because dcls

def wset(i):
	def r(b):
		m=(1<<i)
		c= cursor.prime
		if b:
			c.w|= m
		else:
			c.w&=~m
	return r

def step():
	#motion
	return cursor.step()

def thrust(b,d):
	assert(isinstance(b,bool))
	assert(isinstance(d,ivec2))
	#print(d)
	if b:
		cursor.prime.thrust(b,d)


def emplace(name):
	body(cursor.prime.p, runedict[name])

snake=   lambda p,w:   int(p.y*w+p.x)
snakent= lambda i,w: ivec2(  i%w,i/w)


@dcls
class bound:
	org: ivec2
	dim: ivec2
	def __iter__(self):
		pass #lol
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



def aktivat():
	p= cursor.prime.p
	b= grid.get(p)
	if b==focus or b==None:
		focus= ROOT
		return
	focus(b)
