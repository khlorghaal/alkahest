resolution= (640*3,480*2)
audio_enable=False

_focus= None
def focus(o=0):
	#because intermod globs are fuck
	#fixme subtract retardation
	global _focus
	if o:
		_focus= o
	return _focus

en= enumerate
ra= range
true= True
fals= False
null= None

import sys
from IPython.core import ultratb
sys.excepthook = ultratb.FormattedTB(mode='Plain', color_scheme='Linux', call_pdb=False)

import inspect
srcframe= lambda: inspect.getframeinfo(inspect.currentframe())
srcframe_outer= lambda: inspect.getframeinfo(inspect.currentframe().f_back)
lineno= lambda: srcframe().lineno
lineno_outer= lambda: srcframe_outer().lineno

def warn(s):
	print(f'warn: {lineno_outer()}: {s}')
def  err(s):
	raise AssertionError(f'errr: {lineno_outer()}: {s}')

def ass(v,p,arg=None):
	if v==p:
		return
	raise AssertionError(f'assnt {v} != {p} ; {arg}')

def assT(v,T):
	if type(v)==T:
		return
	raise AssertionError(f'assTnt {type(v)} != {T}\n{v}')

def plocals():
	l= inspect.currentframe().f_back.f_locals.items()
	for s,v in l:
		print(f'{s}:{type(v)}={v}')
		

from dataclasses import dataclass as dcls
immut= dcls(frozen=True)
from enum import Enum
from enum import unique

from math import pi  as PI
from math import tau as TAU
PHI= (1+5**.5)/2
TAU= 2*PI
from math import exp
from math import log2


join2d= lambda a: '\n'.join([''.join(s) for s in a])

flatten2= lambda a: [_ for e in a for _ in e]

from copy import copy
#todo this will later be replaced by a more specialised hierarchical space
#	whatever the fuck that means
@dcls
class ivec2:
	x: int
	y: int
	def __post_init__(self):
		self.x= int(self.x)
		self.y= int(self.y)
	def __getitem__(self, i): 
		if i==0:
			return self.x
		if i==1:
			return self.y
		raise IndexError(i)
	def __iter__(self,i):
		return iter((x,y))
	def __eq__(self,other): return self.x==other.x and self.y==other.y
	def __hash__(self): return hash(self.x)^hash(self.y)


def ivec2op(op):
	op= int.__dict__[op]
	def ret(self, other):
		if type(other)==ivec2:
			return ivec2(
				int(op(self.x,other.x)),
				int(op(self.y,other.y)))
		else:#scalar
			assert(isinstance(self,ivec2))
			assert(isinstance(other,(int,float)))
			return ivec2(
				int(op(self.x,int(other))),
				int(op(self.y,int(other))))
	return ret

arithmetic_list= [
	'__add__','__sub__','__mul__','__floordiv__','__mod__',
	'__divmod__','__pow__','__lshift__','__rshift__','__and__',
	'__xor__','__or__','__neg__','__abs__',
	'__round__','__trunc__','__floor__','__ceil__']
for op in arithmetic_list:
	setattr(ivec2,op,ivec2op(op))