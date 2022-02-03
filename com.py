resolution= (640*3,480*2)
audio_enable=False


en= enumerate
ra= range

from dataclasses import dataclass as dcls
PHI= 1.61803398874
PI= 3.14159265359
TAU= 2*PI

join2d= lambda a: '\n'.join([''.join(s) for s in a])

flatten2= lambda a: [_ for e in a for _ in e]

#todo this will later be replaced by a more specialised hierarchical space
@dcls
class ivec2:
	x: int
	y: int
	def __getitem__(self, i): 
		if i==0:
			return self.x
		if i==1:
			return self.y
		raise IndexError(i)
	def __iter__(self,i):
		return iter((x,y))

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