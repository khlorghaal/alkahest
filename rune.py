'''
runes are the defined chars formed by glyphs
a glyph being an arbitrary raster of the 8x8 cell size
runes may form alphanumeric chars
	typic of traditional langs and fonts
or any atypical named-symbol
	such as novel function forming chars
	and gronks

glyphs may contain non-rune data
	for use as fuckall whatever

this module concerns itself with
mapping glyphs <=> runes

rune data includes
	font data
		optional UTF character
		rune UTF-string name(s)
		the 8x8 raster

	behavior of runes is specified by alkahest via constexprs
		nonconstexpr behavior maps into dynamic types

'''

import numpy
from numpy import array

from com  import *
from math import *

def arrarr_wh(a):
	return (len(a[0]),len(a))

class lib:
	pass
dic={}
#lib.runename
#dic[runename]
#	equivalent

class rune:
	_rune_idit=0
	def __init__(self, names, dat):
		if type(dat)==int:
			self.bin= dat
		else:
			assert(type(dat   )==tuple)
			assert(type(dat[0])==tuple)
			assert(arrarr_wh(dat)==(8,8))

			l= lambda x,y: dat[y][x]<<( x+y*8 )
			r= array([([ l(x,y) for x in ra(8)]) for y in ra(8)])
			self.bin= int(numpy.sum(r,dtype='uint64'))&0xFFFFFFFFFFFFFFFF

		self.names= names
		for n in names:
			setattr(lib,n,self)
			dic[n]= self
		dic[self.bin]= self

	def __str__(self):
		s= self.name
		i= self.bin
		for y in ra(8):
			for x in ra(8):
				lum= ((1<<(x+y*8))&i)!=0
				s+= 'X' if lum else '.'
		return s


def strnrm(pile:list[str,rune]):
	ret=[]
	for e in pile:
		if type(e)==rune:
			ret+= [e]
		elif type(e)==str:
			ret+= [dic[e]]
		else:
			assert(0)
	return ret


def load_font(file):
	import font
	from font import rmf
	f= rmf.load(file)
	assert(f.wh==(8,8))
	for g in f.glyphs.values():
		rune(g.names,g.raster)

load_font('./font/lunatic.rmf')

class tests:
	#import atom

	def font():
		import space
		i=0
		l= dic.values()
		l= tuple({e:None for e in l}.keys())#ordered dup eliminate

		W= 12
		ll= len(l)
		assert(ll<W*W*4)
		for y in ra(-W,W):
			for x in ra(-W,W):
				if i>=ll:
					break
				space.body(ivec2(x,y),l[i])
				i+=1

	def descritpions():#of runes
		import space
		i=0
		l= dic.values()
		l= tuple({e:None for e in l}.keys())
		#ordered dup eliminate
		#set quickly bungles ordering

		for y,r in en(l):
			y= 16-y
			x= -8
			x= (y//64)*32
			y= y%64
			space.body(ivec2(x,y),r)
			names= filter(lambda n: len(n)>1,r.names)
			s= ','.join(names)
			for x_,c in en(s):
				space.body(ivec2(x_+x+2,y),dic[c])

			#atom.text(s,ivec2(x+2,y))
			i+=1
