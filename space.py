from com import *
from rune import rune

grid= {}

class body:
	active=[]
	def __init__(self,pxy,run,z=0,mod=0):
		assert(type(pxy)==ivec2)
		self.p= pxy
		self.z= z#z currently only used for UI layer
		if(type(run)==str):
			run= rune.lib[run]
			assert(run!=None)
		assert(type(run)==rune)
		self.rast= run.bin
		self.rune= run
		self.mod= mod

		body.active.append(self)
		if pxy in grid:
			body.active.remove(grid[pxy])
		grid[pxy]= self

	def kill(a):
		if type(a)==ivec2:
			p=a
			b=grid[p]
		elif type(a)==body:
			p= a.p
			b= a
		else:
			raise 'bargT' #obvious
		body.active.remove(b)
		grid.pop(p)

origin= body(ivec2(0,0),rune.lib['empty'])

class cursor:
	insts=[]
	prime= None
	def __init__(self,p):
		self.v= ivec2(0,0)
		self.w=0
		self.body= body(p,rune.lib['border'])
		#FIXME dont use a body, as bodies are spatial mutex
		#this is fucky UB as body position should be immut
		#also implying a needed refactor of bodies

		self.vel_active=0
		cursor.insts+=[self]

	def thrust(self,b,d):
		if self.vel_active:
			self.v= d if b else -d
		elif b:
			self.body.p+= d*(1<<self.w)
			#print(self.body.p)
	def step():
		for c in cursor.insts:
			if c.vel_active:
				throw#fixme
				c.body.p+= c.v*(1<<z)
cursor.prime= cursor(ivec2(0,0))

def wset(i):
	def r(b):
		m=(1<<i)
		c= cursor.prime
		if b:
			c.w|= m
		else:
			c.w&=~m
	return r
w0= wset(0)
w1= wset(1)
w2= wset(2)
w3= wset(3)

def step():
	#motion
	cursor.step()

def thrust(b,d):
	assert(isinstance(b,bool))
	assert(isinstance(d,ivec2))
	print(d)
	if b:
		cursor.prime.thrust(b,d)

def insert_cur(s):
	body(cursor.prime.p,rune.lib[str])

def emplace(name):
	body(cursor.prime.body.p, rune.lib[name])

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


#vesicle: a data ownership construct
#may be fractally contained within other vescicles
#bounds may overlap, vescicles may not
#	being contained is not considered overlapping
#	the set intersection of A,B must equal A or B or None
@dcls
class vesc:
	bnd: bound
	def validate(self):
		raise 'ohno'
	def kill(self):
		for body,p in bnd:
			body.kill()
