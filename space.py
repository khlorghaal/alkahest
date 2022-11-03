#space is grid and mapping of ordinates onto objects
#space does not concern itself with the behavior of contained objects
#	only mapping of intoactions onto objects

from com import *
from rune import dic as runedic
from rune import rune
from rune import glyph

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
	rune: rune
	z: int=0 #layer, only 0 is nonvolatile (serialized)
	mod: int=0 #modifier visual status
	ptr: object= None #dynamic datum

	h= lambda s:(s.p,s.z)

	def __post_init__(self):
		h= self.h()
		o= grid.pop(h,None)
		o and o.kill()
		grid[h]= self

	def kill(self):
		grid.pop(self.h(),None)
		ptr= self.ptr
		ptr and ptr.kill and ptr.kill()



def kill(p:ivec2,z:int=0):
	g= grid.get((p,z))
	if g:
		g.kill()

def search_emplace():
	#create and focus gui
	pass
	#destruct


origin= body(ivec2(0,0),runedic['empty'])

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
		b= (grid[(p_,self.z)] for p_ in p)
		return zip(b,p)
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
		for p in bound(ivec2(0,-4),ivec2(1,8)):
			body(p,runedic['coplanrect'],i,0)




filename= 'default.grid.png'

def load():
	from numpy import array
	from numpy import zeros
	from numpy import flip
	from numpy import uint8
	import png

	try:
		w,h, img, meta= png.Reader(filename).read()
	except:
		print('gridfile not found')
		return

	ass(w%8,0)
	ass(h%8,0)
	ass(meta['bitdepth'],1)
	ass(meta['planes'  ],1)

	rast= array(list(img),dtype=uint8).transpose()
	rast= flip(rast,1)

	for y in ra(0,h,8):
		for x in ra(0,w,8):
			n=0
			for ry in ra(8):
				for rx in ra(8):
					i=rast[x+rx,
					       y+ry]
					i= int(i==1)
					n|= i<<(rx+ry*8)
			if n!=0:
				if n in runedic:
					body(ivec2(x//8,y//8),runedic[n])
				else:
					body(ivec2(x//8,y//8),glyph(n))
					continue#warn('rune not in dict 0x%16x'%n)

	print('loaded %s'%filename)

def save():
	from numpy import array
	from numpy import zeros
	from numpy import uint8
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
	rast= zeros((w,h),dtype='uint8')
	for b in grid.values():
		if b.z!=Z:
			continue
		i= int(b.rune.bin)
		#print('{0:064b}'.format(i))
		p= b.p*8
		for ry in ra(8):
			for rx in ra(8):
				#snake
				on= ((1<<(rx+ry*8))&i)!=0
				rast[
					   rx+p.x-o.x,
					   ry+p.y-o.y
					]= on

	rast= rast.transpose().flatten()
	rast= flip(rast,1)

	#print(rast)
	img= png.Writer(
		w,h,
		bitdepth=1,
		greyscale=True,
		alpha= False,
		compression=2
		)
	img.write_array( open('default.grid.png','wb'), rast.flatten() )
	print('saved %s'%filename)

