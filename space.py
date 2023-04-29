#space is grid and mapping of ordinates onto objects
#space does not concern itself with the behavior of contained objects
#	only mapping of intoactions onto objects

from com import *
from rune import dic as runedic
from rune import lib as runelib
from rune import rune
from rune import glyph
from enum import Enum as enum

grid= {}

#assume whatever the fuck this is can be ignored
#bitmaskfield (very fucky)
#mod bits
#max=32
#Sb e? (name|enum) (//(comment))? #what??
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
_i=0
def i(n=1):
	global _i
	r=_i
	_i+=n
	return ((1<<n)-1)<<r

mods= {
	'none':     0,
	'bland':    i(),
	'aktiv':    i(),
	'unaktiv':  i(),
	'verboten': i(),
	'spicey':   i(),
	'highlight':i(),
	'achtung':  i(),
	'warning':  i(),
	'danger':   i(),
	'primary':  i(),
	'cursor':   i(),
	'smol':     i(),
	'proj':     i(2),#ortho,parallax,perspective,skew
	'axp':      i(4),#right //arity-count per side [0, 1<<4 = 8 ]
	'axn':      i(4),#left
	'ayp':      i(4),#north
	'ayn':      i(4),#south
	'rot':      i(2),#rotation, cardinal [0,1,2,3]->[right,north,left,south]
}
class mod:
	pass
for k,v in mods.items():
	setattr(mod,k,v)
del i


@immut
class body:
	p: ivec2
	glyph: glyph
	z: int=0 #layer, only 0 is nonvolatile (serialized)
	#negative z is useful for second layer of same zoomlevel
	mod: int=0 #modifier visual status
	ptr: object= None #dynamic datum
	align: ivec2= ivec2(0,0)
	h= lambda s:(s.p,s.z)

	def __post_init__(self):
		assT(self.p,ivec2)
		assT(self.glyph,glyph)
		h= self.h()
		o= grid.pop(h,None)
		o and o.kill()
		grid[h]= self

	def kill(self):
		grid.pop(self.h(),None)
		ptr= self.ptr
		ptr and ptr.kill and ptr.kill()

	#remake body with a rune if glyph matches one
	def rune(self):
		return runedic.get( self.glyph.bin,runelib.empty )

	def __str__(s):
		return f'{s.p} {str(s.glyph)} {s.z} {s.mod} {str(s.ptr)}'

#alt ctors
def body_s(p:ivec2, s:str , z:int=0, mod:int=0,ptr:object=None, align=ivec2(0,0)):
	assT(s,str)
	return body(p,  runedic.get(s,runelib.empty).gph, z=z, mod=mod, ptr=ptr, align=align )
def body_r(p:ivec2, r:rune, z:int=0, mod:int=0,ptr:object=None, align=ivec2(0,0)):
	assT(r,rune)
	return body(p,  r.gph,  z=z,       mod=mod,      ptr=ptr,                 align=align )

def kill(p:ivec2,z:int=0):
	g= grid.get((p,z))
	g and g.kill()

def search_emplace():
	#create and focus gui
	pass
	#destruct


origin= body_r(ivec2(0,0),runelib.dashborder, 2, mods['bland'])

snake=   lambda p,w:   int(p.y*w+p.x)
snakent= lambda i,w: ivec2(  i%w,i/w)


@dcls
class bound:
	org: ivec2
	dim: ivec2
	z=0
	def __iter__(self):#snake
		x0= self.org.x
		y0= self.org.y
		x1= self.org.x+self.dim.x
		y1= self.org.y+self.dim.y
		p= (ivec2(x,y) for y in range(y0,y1) for x in (range(x0,x1)))
		b= (grid.get((p_,self.z)) for p_ in p)
		return zip(b,p)#body, position
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
			x1-x0+1,#+1 because inclusive
			y1-y0+1)
		return bound(ivec2(x0,y0),ivec2(w,h))

	def kill(self):
		for body,p in self.__iter__():
			body.kill()


def aktivat(de):
	b= grid.get(cursor.prime.b.h())
	b= b==focus() or b==None
	focus( b if b else de )

def tests():
	#z
	for i in range(-4,4):
		for b,p in bound(ivec2(0,-4),ivec2(1,8)):
			body_s(p,'coplanrect',0,0)




filename= 'world.grid.txt'

def load():
	from numpy import array
	from numpy import zeros
	from numpy import flip
	from numpy import uint8
	import png

	try:
		f= open(filename,'r')
		f= list(f)
	except:
		warn('gridfile not found')
		return

	#flip y;
	f= f[::-1]
	w= len(f[0])-1
	h= len(f)
	#trailing \n is not a newline, it is not ''

	rast=[]
	for l in f:
		#str->[chr]->[bool]
		l= l[:-1]#trim \n
		l= [c not in '. _□0' for c in l]
		ass(len(l),w)
		rast+= [l]

	ass(w%8,0)
	ass(h%8,0)

	#load all as glyphs
	for y in ra(0,h,8):#tile iteration
		for x in ra(0,w,8):
			n=0
			for ry in ra(8):#glyph bits
				for rx in ra(8):
					i=rast[y+ry]\
					      [x+rx]
					i= int(i==1)
					n|= i<<(rx+ry*8)
			if n!=0:
				body(ivec2(x//8,y//8),glyph(n))

	print('loaded %s'%filename)

def save():
	from numpy import array
	from numpy import zeros
	from numpy import uint8
	from numpy import flip
	import png

	Z= 0 #z 0 is only nonvolatile layer saved
	bnd= bound.compute(
		list(filter(
			lambda b: b.z==Z,
			grid.values())))
	(w,h)= (
		bnd.dim.x*8,
		bnd.dim.y*8)
	o= bnd.org*8
	#print(b)
	if w==0 or h==0:
		return
	rast= zeros((w,h),dtype='uint8',col='F')
	for b in grid.values():
		if b.z!=Z:
			continue
		gph= int(b.glyph.bin)
		#print('{0:064b}'.format(i))
		p= b.p*8 - o
		for ry in ra(8):
			for rx in ra(8):
				#snake
				i= rx+ry*8
				on= ((1<<i)&gph)!=0
				rast[
					   rx+p.x,
					   ry+p.y
					]= on

	#no fucking idea why its transposed
	#dont know if numpy is transposing it or the iteration
	rast= flip(rast,0)

	with open(filename,'w') as f:
		for l in rast:
			for c in l:
				c= '.' if not c else '■'
				f.write(c)
			f.write('\n')
	ass()
	print('saved %s'%filename)

