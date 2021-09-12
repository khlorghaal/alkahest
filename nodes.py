from typing import Iterable
from itertools import chain
from functools import reduce as fold
from operator import add



class terminal(list):
	#prevents list descent, lisp quot analogue
	#used if you want leaf content to be trees
	def __init__(self,*v):
		super().__init__(v)
leafy= lambda l: isinstance(l,terminal) or isemptylist(l) or not isinstance(l,Iterable) or isinstance(l,str)

class cons:
	def __init__(self,v,c):
		self.v= v
		self.c= c

pass_t= object()#placeholder
def tremove_cond(t,c):

	if not c(n,d,i):

tremove_valu_eq = lambda t,v: tremove_cond    (t, lambda n: n==v)
tremove_valu_neq= lambda t,v: tremove_cond    (t, lambda n: n!=v)
tremove_pass=     lambda t  : tremove_valu_neq(t, pass_t)

#leafs
#	inherently always have data
#	which may be null or an empty set
#branches
#	branches have no content, only children
#	the content returned per branch is the result of the lambda
#	a branch is not a cons, but the returned tree is
tmap_leaf      = lambda f,n        :                 f(n    ) if leafy(n ) else [tmap_leaf  (f,n_       ) for    n_ in           n ]
tmap_leaf_ndi  = lambda f,n,d=0,i=0:                 f(n,d,i) if leafy(n ) else [tmap_leaf  (f,n_,d+1,i_) for i_,n_ in enumerate(n)]
tmap_branch    = lambda f,n        :  tremove_pass([   pass_t if leafy(n_) else  tmap_branch(f,n_       ) for    n_ in           n ])
tmap_branch_ndi= lambda f,n,d=0,i=0:  tremove_pass([   pass_t if leafy(n_) else  tmap_branch(f,n_,d+1,i_) for i_,n_ in enumerate(n)])

#tmap_both=   lambda fl,fb, n,d=0,i=0:  ??? if leafy(n_) else ???

isemptylist= lambda l: l==[] or l==() or l=={}
tnullish= lambda l: tmap_leaf(lambda n,d,i: n==None or isemptylist(n), l)

tflat= lambda n: [n] if leafy(n) else [ l for i in n for l in tflat(i)] #return nodes as a non-nested 1D list

tsum=    lambda l: fold(add,tflat(l))
tmax=    lambda l: fold(max,tflat(l))

tstrflat= lambda n: tsum(tmap_leaf(lambda n_,d,i: '%s'%n_,n))
tstrgrid= lambda n: '0'

#tests

tr= [0,1,[0,1,2],[3],[[4]],[[[5]]],['a','b']*2, [[['x'],'y'],'z'], ['i',['j',['k']]],
	[],  [[]],  [[[]]],  [[],[]],  [[[]],[[]]],  [[[[[[]],[[]]]],[[[[]],[[]]]]]]
	]
trflat= tflat(tr)
LCT= len(trflat)#leaf count
NCT= len(tflat(tmap_branch(lambda n,d,i: None ,tr)))#node count
ND =           tmap_branch(lambda n,d,i:    d ,tr)  #node depth
NLN=           tmap_branch(lambda n,d,i:len(n),tr)  #node lenth

print('PYP  %s'%tr)
print('PPF  %s'%trflat)

print('LCT %3i'%LCT)
print('NCT %3i'%NCT)
print('ND  '   +tstrflat(ND) )
print('NLN '   +tstrflat(NLN))


print('ALL\n N  D  CI| IND')
info=lambda n,d=0,i=0,x=[]: terminal(n,d,i,x) if leafy(n) else [info(n_,d+1,i_,x+[i_]) for i_,n_ in enumerate(n)]
ALL= info(tr)
print(tstrgrid(ALL))


#W= tmax(tmap_leafy(lambda n,d,i: ?? ,info))
#H= tmax(NL)
#print('W:%i H:%i'%(W,H))

#raster
#rast= [terminal([0]*W) for _ in range(H)]
#print(tstrgrd(rast))


