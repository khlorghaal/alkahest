#hyperdimensional numerals via space filling curve

from com  import *
from math import *
en=enumerate
ra=range

w=3#param
b=1#border
q=w+b
#n=w*w+1#combo
n=2<<w
a= n*q
rast=[[(x,y)for x in ra(a)]for y in ra(a)]
for r,l in en(rast):
	for c,v in en(l):
		x =c %q
		y =r %q
		gx=c//q
		gy=r//q
		i = x+ y*w#snakes
		g =gx+gy*n
		b= g&(1<<i)
		if x<w and y<w:
			ch= '▉'if b else' '
		else:
			ch= '.'
		rast[r][c]= ch
		
print(join2d(rast[::-1]))
