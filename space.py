from com import *
from numpy import array
import gl_backend

class ori:
	rast=[[1]]
	p= array((0,0))
class cur:
	p= array((0,0))
	v= array((0,0))
	w=0
	rast=[
		[1,1,1],
		[1,0,1],
		[1,1,1],
	]
	vel_active=0
	def thrust(d):
		if cur.vel_active:
			cur.v= cur.d
		else:
			cur.p+= d*(1<<cur.w)
def wset(i):
	def r(b):
		m=(1<<i)
		if b:
			cur.w|= m
		else:
			cur.w&=~m
	return r
w0= wset(0)
w1= wset(1)
w2= wset(2)
w3= wset(3)

geoms=[
	cur,
	#ori,
	]
shash={}

def step():
	#motion
	if cur.vel_active:
		throw#fixme
		cur.p+= cur.v*(1<<z)
def render():
	gl_backend.tr= cur.p
	for g in geoms:
		gl_backend.quad(g.p,0,g.w,0xAFFFFF8F)

def thrust(b,d):
	if b:
		d= array(d)
		cur.thrust(d)