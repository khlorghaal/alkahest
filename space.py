from com import *
from rune import rune

class body:
	active=[]
	def __init__(self,pxy,z,r):
		assert(type(pxy)==ivec2)
		self.p= pxy
		self.z= z#z currently only used for UI layer
		assert(type(r)==rune)
		self.rune= r

		body.active.append(self)

origin= body(ivec2(0,0),0,rune.lib.solid)

class cursor:
	insts=[]
	prime= None
	def __init__(self,p):
		self.v= ivec2(0,0)
		self.w=0
		self.body= body(p,0,rune.lib.border)

		self.vel_active=0
		cursor.insts+=[self]

	def thrust(self,b,d):
		if self.vel_active:
			self.v= d if b else -d
		elif b:
			self.body.p+= d*(1<<self.w)
			print(self.body.p)
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
	if b:
		cursor.prime.thrust(b,d)