from com import *
from numpy import array
import gl_backend

class ori:
	rast=[[1]]
	p= array((0,0))
class cur:
	p= array((0,0))
	v= array((0,0))
	rast=[
		[1,1,1],
		[1,0,1],
		[1,1,1],
	]
	vel_active=0

geoms=[
	cur,
	#ori,
	]
shash={}

def step():
	#motion
	if cur.vel_active:
		cur.p+= cur.v
def render():
	gl_backend.tr= cur.p
	for g in geoms:
		gl_backend.quad(g.p,0)

def thrust(b,d):
	if b:
		d= array(d)
		if cur.vel_active:
			cur.v= d
		else:
			cur.p+= d