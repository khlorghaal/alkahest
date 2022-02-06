from com import *
from rune import rune

grid= {}

class body:
	active=[]
	def __init__(self,pxy,run,z=0,mod=0):
		assert(type(pxy)==ivec2)
		self.p= pxy
		self.z= z#z currently only used for UI layer
		assert(type(run)==rune)
		self.rast= run.bin
		self.rune= run
		self.mod= mod

		body.active.append(self)
		if pxy in grid:
			body.active.remove(grid[pxy])
		grid[pxy]= self

origin= body(ivec2(0,0),rune.lib['empty'])

class cursor:
	insts=[]
	prime= None
	def __init__(self,p):
		self.v= ivec2(0,0)
		self.w=0
		self.body= body(p,rune.lib['border'])

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