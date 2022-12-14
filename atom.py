'''
logic of runes with behavior

sigils are entry points

remember- when writing docs when high, provide a translation

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

'''

from com import *
from space import *
import rune

import transpiler


@dcls
class cursor:
	v:ivec2= ivec2(0,0)
	vel_active:bool= 0
	b: body= 0
	zoom= 2 #unrelated to body-z
	#magnification by 1<<zoom
	#big zoom == big glyphs

	word:str= ''#accumulator for multichars
	#	multichars being a rune with a name longer than 1 character
	#	may also map onto any of multiple names per rune

	def __post_init__(s):
		s.move(ivec2(0,0))
		cursor.insts+=[s]

	def zoomd(s, d):#differential
		z=s.zoom
		z+= d
		z= max(z,0)
		z= min(z,4)
		s.zoom=z

	def move(s,p:ivec2):
		if s.b:
			s.b.kill()
		s.b= body(
			p,
			runedic['cursor'].gph,
			1,
			mods['cursor'])

	def emit(s,r):
		if type(r)==str:
			r= runedic[r]
		else:
			assert(type(r)==rune.rune)
		body(s.b.p,r,0)

	def step():
		r=None#dirty
		for c in cursor.insts:
			if c.v!=ivec2(0,0):
				r= True
				d= c.v
				c.v*=0#halt
				c.move(c.b.p+d)
		return r
	def thrust(d:ivec2):
		cursor.prime.v+= d

setattr(cursor,'insts',[])
setattr(cursor,'prime',cursor())#because dcls




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
		return todo

	def fromstr(bnd,s):
		t= text(bnd)
		s= s.strip('\t').split(' ')
		for c in s:
			t.inp(1,c,0)
		return t


	def inp(self,b,ch,sc):
		if not b:
			return
		p= self.cur.b.p
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
		self.cur.move(p)

		if ch=='\b':
			g= grid.get(p)
			if g:
				g.kill()

@dcls
class raster:#the entity
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

'''
entry point for
	eval
		manual invocation through cursor
			void-ary
				cursor in the future may carry state?
		emits output to console
	loop
		monoidal
			states emitted at end, repassed to self
		initiated with
		python method of outer-eval passing initial state
		emits output via
			impure functions
			media (displays, audio, text, etc)
	api
		todo some decorator bullshit idk
		abi socketed through python, until python subsumed


switch of these is determined by subrunes
	direction is too ambiguous and messy, rejected


possible approaches for mode selection
	-outer functor, with sigil as input
	-subrunes, of the sigil itself
	-constex inputs, as double-lambda
		ie sigil(mode.loop)(initstate)

	subrunes selected for being most sorcerous
		functors may operate on sigils to change subrunes
			this can and will be messy but whatever

'''
@dcls
class sigil:
	body_main: body #the sigil itself
	body_args: list[body] #macro parameters
	entry: body #first runes evaluated

	def eval(self):
		#the sigil itself
		self.body_main

		#sigil behavior
		self.body_args
		self.entry





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
		#space.cursor.prime.move(t.bnd.org)

		#cursor.prime.p= ivec2(-8,-8)
		#eval()




def step():
	#motion / time-integration
	return cursor.step()
'''
focus membrane
repl
get data 
'''
