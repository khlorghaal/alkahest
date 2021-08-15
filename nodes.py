from typing import Iterable
from itertools import chain
from functools import reduce as fold
import operator



class terminal(list):
	#prevents list descent, lisp quot analogue
	#used if you want leaf content to be trees
	def __init__(self,*v):
		super().__init__(v)
leafy= lambda l: isinstance(l,terminal) or l==[] or l==() or l=={} or not isinstance(l,Iterable) or isinstance(l,str)

class cons(tuple):
	def __init__(self,v,c):
		super().__init__([v,c])
	@property
	def foo(self): return self[0]
	@property
	def   c(self): return self[1]

#leafs
#	inherently always have data
#	which may be null or an empty set
#map branches
#	branches have no content, only children
#	the content returned per branch is the result of the lambda
#	a branch is not a cons, but the result tree is

tmap_leaf=   lambda f,n,d=0,i=0:  f(n,d,i) if leafy(n) else               [tmap_leaf  (f,n_,d+1,i_) for i_,n_ in enumerate(n)]
tmap_branch= lambda f,n,d=0,i=0:        [] if leafy(n) else cons(f(n,d,i),[tmap_branch(f,n_,d+1,i_) for i_,n_ in enumerate(n)])

tnullish= lambda l: tmap_leaf(lambda n,d,i: n!=None and not isinstance(n,Iterable), l)
#tvalid= whatever the fuck you want is valid

tflat= lambda n: [n] if leafy(n) else [ l for i in n for l in tflat(i)] #what

tsum=    lambda l: fold(operator.add,tflat(l))
tmax=    lambda l: fold(         max,tflat(l))

strang= lambda n: '%2s'%n if leafy(n) else ['%2s'%s for s in n]
tstr= lambda nl: lambda l: nl.join(tflat(tmap_leafy(lambda n,d,i: strang(n), l)))
tstrcat= tstr(' ')
tstrgrd= tstr('\n')


cast_tree_cons= 

cmap= 



#vvv tests vvv



tr= [0,1,[0,1,2],[3],[[4]],[[[5]]],['a','b']*2, [[['x'],'y'],'z'], ['i',['j',['k']]],
	[],  [[]],  [[[]]],  [[],[]],  [[[]],[[]]],  [[[[[[]],[[]]]],[[[[]],[[]]]]]]
	]
trflat= tflat(tr)
print('PYP  %s'%tr)
print('PPF  %s'%trflat)

LCT= len(trflat)#leaf count
NCT= tsum(tmap_branch(lambda n,d,i:1,tr)) #node count
ND =      tmap_branch(lambda n,d,i:    d ,tr)#node depth
NLN=      tmap_branch(lambda n,d,i:len(n),tr)#node lenth
print('LCT %3i'%LCT)
print('NCT %3i'%NCT)
print('ND  '   +tstrcat(ND ) )
print('NLN '   +tstrcat(NLN) )


print('ALL\n N  D  CI| IND')
info=lambda n,d=0,i=0,x=[]: terminal(n,d,i,x) if leafy(n) else [info(n_,d+1,i_,x+[i_]) for i_,n_ in enumerate(n)]
ALL= info(tr)
ALL= map(tstrcat,ALL)
print(tstrgrd(ALL))



#W= tmax(tmap_leafy(lambda n,d,i: ?? ,info))
#H= tmax(NL)
#print('W:%i H:%i'%(W,H))

#raster
#rast= [terminal([0]*W) for _ in range(H)]
#print(tstrgrd(rast))
