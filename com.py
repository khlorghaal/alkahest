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

from dataclasses import dataclass as dcls
immut= dcls(frozen=True)

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

for op in [
	'__add__','__sub__','__mul__','__floordiv__','__mod__',
	'__divmod__','__pow__','__lshift__','__rshift__','__and__',
	'__xor__','__or__','__neg__','__abs__',
	'__round__','__trunc__','__floor__','__ceil__']:
	setattr(ivec2,op,ivec2op(op))