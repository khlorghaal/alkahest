#pos= lambda tree: [n() for n in tree]
from typing import Iterable

leafy= lambda l: ~(isinstance(l,Iterable) and not isinstance(l,str))
jl= lambda l:''.join(['%2s'%s for s in l])

nprint= lambda n,d,i: print('%2s %i %i'%(str(n),d,i))
def tmap(f,t,d=0,i=0):
	dp= d+1
	if leafy(t):
		f(t,d,i)
	else:
		for i_,n in enumerate(t):
			tmap(f,n,dp,i_)

#tr= [[['a'],'b'],'c']
tr= [0,1,[0,1,2,3],[0],[[0]],[[[0]]],['a','b']*2]
print('PYPR')
print(tr)
print('TRPR\n n d i')
tmap(nprint,tr)
#tmap( lambda n: [chr(ord(c)+1) for c in n], tr)


#object stats
def total_leaf(n,d,i):
	total_leaf.sum+=1
total_leaf.sum=0
tmap(total_leaf,tr)
print('LCT %3i'%total_leaf.sum)

def total_node(t,d=0,i=0):
	total_node.sum+= 1
	if not leafy(t):
		dp= d+1
		for i_,n in enumerate(t):
			total_node(n,dp,i_)
total_node.sum= 0
total_node(tr)
print('NCT %3i'%total_node.sum)

def depths(n,d=0,i=0):
	if leafy(n):
		depths.l+=[d]
	else:
		dp= d+1
		for i_,n in enumerate(n):
			depths(n,dp,i_)
depths.l= []
depths(tr)
print('LDP '+jl(depths.l))


def lengths(n,d=0,i=0):
	if not leafy(n):
		lengths.l+=[len(n)]
		dp= d+1
		for i_,n in enumerate(n):
			lengths(n,dp,i_)
lengths.l= []
lengths(tr)
print('LEN '+jl(lengths.l))


#raster
rast= [[0]*16 for _ in range(8)]
rpl= 0
def rput(n,d,i):
	#rast[0][0]=n
	global rpl
	rast[i][d]= n
	rpl+=1
tmap(rput,tr)
sacc= ''
for l in rast:
	sacc+= jl(l)
	sacc+= '\n'
print('RST')
print(sacc)


#list of index descents per leaf
def indxs(n,p):
	if leafy(n):
		indxs.l+= [p]
	else:
		for i,n_ in enumerate(n):
			indxs(n_,p+[i])
indxs.l= []
indxs(tr,[])
print('IND')
print(indxs.l)