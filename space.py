from com import *
from rune import dic as runedic
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
_i=0
def i(n=1):
	r=i
	i+=n
	return ((1<<n)-1)<<r

mods= {
	'none':      0,
	'bland':     1<<i(),
	'aktiv':     1<<i(),
	'unaktiv':   1<<i(),
	'verboten':  1<<i(),
	'spicey':    1<<i(),
	'highlight': 1<<i(),
	'achtung':   1<<i(),
	'warning':   1<<i(),
	'danger':    1<<i(),
	'primary':   1<<i(),
	'cursor':    1<<i(),
	#ortho,parallax,perspective,skew //projection
	#axp3 //arity-count per side [0,8]
	#axn3 //where 0u is void-ary 
	#ayp3 //      4u is 16-ary
	#ayn3 
	#rot2 rotation, cardinal
	'a'=    i(2)
	'h'=    i(1)
	'v'=    i()
	'p'=    i()
	'c'=    i()
	'w'=    i(2)
	'w0'=   i()
	'axp' = i(3)
	'axp0'= i()
	'axn' = i(3)
	'axn0'= i()
	'ayp' = i(3)
	'ayp0'= i()
	'ayn' = i(3)
	'ayn0'= i()
	'rot' = i(2)
	'rot0'= i()
	'smol'= i()
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
	z: int=0
	mod: int=0
	ptr: object= None

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

origin= body(ivec2(0,0),runedic['empty'])

@dcls
class cursor:
	v:ivec2= ivec2(0,0)
	vel_active:bool= 0
	b: body= 0
	z= 0#zoom, unrelated to body-z
	word:str= ''#accumulator for multichars
	#multichars being a rune with a name longer than 1 character

	def __post_init__(s):
		s.place(ivec2(0,0))
		cursor.insts+=[s]

	def zoom(s, d):
		z=s.z
		z+= d
		z= max(z,0)
		z= min(z,4)
		s.z=z

	def place(s,p):
		if s.b:
			s.b.kill()
		s.b= body(
			p,
			runedic['cursor'],
			1,
			mods['cursor'])

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

#prime cursor pos
curppos= lambda: cursor.prime.b.p
curpz=   lambda: cursor.prime.b.z


def thrust(d:ivec2):
	cursor.prime.v+= d


def deplace():
	g= grid.get((cursor.prime.b.p,0))
	if g:
		g.kill()
def emplace(name):
	body(cursor.prime.b.p, runedic[name])

def search_emplace():
	#create and focus gui
	pass
	#destruct

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
		b= (grid[(p_,z)] for p_ in p)
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
	if 0:
		for i in range(-4,4):
			for p in bound(ivec2(0,-4),ivec2(1,8)):
				body(p,runedic['coplanrect'],i,0)

filename= 'default.grid.png'

def load():
	from numpy import array
	from numpy import zeros
	import png
	try:
		img= png.Reader(filename).read()
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
				if b in runedic:
					body(ivec2(x,y),runedic[b])
				else:
					print('warn, rune not in dict 0x%16x'%b)
	print('loaded %s'%filename)

def save():
	from numpy import array
	from numpy import zeros
	from numpy import uint16
	from numpy import uint64
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
	print('saved %s'%filename)

def step():
	#motion
	return cursor.step()