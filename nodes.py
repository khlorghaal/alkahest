from typing import Iterable
from itertools import chain
from functools import reduce as fold
import operator

tr= [0,1,[0,1,2],[3],[[4]],[[[5]]],['a','b']*2, [[['x'],'y'],'z'], ['i',['j',['k']]]]
print('PYP  %s'%tr)


class terminal(list):
	#prevents list descent, lisp quot analogue
	#used if you want leaf content to be trees
	def __init__(self,*v):
		super().__init__(v)
leafy= lambda l: not isinstance(l,Iterable) or isinstance(l,terminal) or isinstance(l,str)

#leafs and nodes
#nodes may or may not have data
#leafs inherently always have data, which may be null; a leaf of an empty set is unpossible
tmap_leafy= lambda f    ,n,d=0,i=0:  f(n,d,i) if leafy(n) else            [tmap_leafy(f    ,n_,d+1,i_) for i_,n_ in enumerate(n)]
tmap_leafn= lambda f    ,n,d=0,i=0:        [] if leafy(n) else ( f(n,d,i),[tmap_leafn(    f,n_,d+1,i_) for i_,n_ in enumerate(n)])
tmap_bisex= lambda fl,fn,n,d=0,i=0: fl(n,d,i) if leafy(n) else (fn(n,d,i),[tmap_bisex(fl,fn,n_,d+1,i_) for i_,n_ in enumerate(n)])

#empty [] is comparable to something between void and none

tflat= lambda n: [n] if leafy(n) else [ l for i in n for l in tflat(i)]

tsum=    lambda l: fold(operator.add,tflat(l))
tmax=    lambda l: fold(max,tflat(l))
strang= lambda n: '%2s'%n if leafy(n) else ['%2s'%s for s in n]
tstr= lambda nl: lambda l: nl.join(tflat(tmap_leafy(lambda n,d,i: strang(n), l)))
tstrcat= tstr(' ')
tstrgrd= tstr('\n')


LCT= len(tflat(tr)) #leaf count
NCT= tsum( tmap_leafn(lambda n,d,i:1 ,tr)) #node count
ND = tmap_leafn(lambda n,d,i:    d ,tr)#node depth
NLN= tmap_leafn(lambda n,d,i:len(n),tr)#node lenth
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
