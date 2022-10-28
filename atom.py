'''
runes or vescicles which cannot be composed from others

the naive witnesses indivision
yet there is further nature
advance onto the nuclear forge
violate composability for true power
	what the fuck was i talking about?

a name is merely location
a location within chaos is necessarily phenoumenal
a name cannot be a true symbol

goedel's incompleteness applies to the arithmetic of language

a name within pure environment, is a z-tunnel between namespace layers
completeness requires name as a static location or static boundary

i need to stop writing docs while high
'''

from com import *
from space import *
import rune

import transpiler

#word: str= ''

@dcls
class text:
	bnd: bound
	editable: bool= False
	wrap: bool= True
		#if wrap is off, the vescicle will attempt expanding +x
		#if it cannot exapand, it will wrap
	cur: cursor= None
	def __post_init__(self):
		self.cur= cursor(self.bnd.org)#default args are static init
		self.cur.rune= rune.dic['|']

	def str(self):
		return str('o nyo??')

	def fromstr(bnd,s):
		t= text(bnd)
		s= s.strip('\t').split(' ')
		for c in s:
			t.inp(1,c,0)
		return t


	def inp(self,b,ch,sc):
		if not b:
			return
		p= self.cur.p
		o= self.bnd.org 
		w= self.bnd.dim.x

		if ch=='\b':
			d= -1
		elif ch=='\n':
			d= w-p.x
		else:
			d= 1
			r= rune.dic.get(ch,None)
			if not r:
				return
			body(copy(p),r)

		#todo expansion bound checks
		#todo wrapping

		p= snakent(d+snake(p*ivec2(1,-1)-o,w),w)*ivec2(1,-1)+o
		#p.x+= d
		self.cur.p= p

		if ch=='\b':
			g= grid.get(p)
			print(g)
			if g:
				g.kill()

@dcls
class raster:
	@unique
	class colorform(Enum):
		NATIVE=0#sRGB8
		MONOCHROME=1#stencil
		GREY=2#R8
		HDR=3#RGBAf16

	bnd: bound
	form: colorform

_proc_loops=[]
def _loop():
	for e in _proc_loops:
		e.invoke()

@dcls
class proc:
	bnd: bound

	def invoke(self):
		transpiler.repl()

	def loop(self,rate:int):
		_proc_loops+=[self]

	def kill(self):
		_proc_loops.remove(self)

def eval():
	#ran on either a boundary or proc
	#on a proc would allow precompile
	#on a raw boundary would be interpreter only
	p= curppos()
	z= 0
	b= grid[(p,z)]
	bnd= b.ptr and type(b.ptr)==bound and b.ptr
	if not bnd:
		return 1

	x0= self.org.x
	y0= self.org.y
	x1= self.org.x+self.dim.x
	y1= self.org.y+self.dim.y
	
	l= [[grid.get((ivec2(x,y),z)) for x in ra(x0,x1)] for y in ra(y0,y1)]
	transpiler.rep(l)


def tests():
	if 1:#textbox
		b= bound(ivec2(0,0),ivec2(16,4))
		t= text(b,True)
		focus(t)

	if 0:#transpiler
		b= bound(ivec2(-8,-8),ivec2(8,8))
		#p= proc(b)
		#p.invoke()

		t= text.fromstr(b,'''
		1 1 1
		add add
		''')
		#space.cursor.prime.place(t.bnd.org)

		#cursor.prime.p= ivec2(-8,-8)
		#eval()



'''
focus membrane
repl
get data 
'''
