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

def aawh(a):
	return (len(a[0]),len(a))

class lib:
	pass
dic={}
#lib.runename
#dic[runename]
#	equivalent

@immut
class glyph:
	bin: int

	def __post_init__(self):
		ass(type(self.bin),int)

	def new(d:tuple[tuple]):
		ass(aawh(d),(8,8))
		b=0
		for y in ra(8):
			for x in ra(8):
				b+= d[y][x]<<( x+y*8 )
		assert(b<(1<<65))
		return glyph(b)


	def __str__(self):
		s= ''
		i= self.bin
		for y in ra(8)[::-1]:
			for x in ra(8):
				lum= ((1<<(x+y*8))&i)!=0
				s+= '█' if lum else '▒'
			s+='\n'
		r= ''
		if i in dic:
			r= dic[i].names
		return f'{i} {r}\n{s}'

def rastint(r:list[list[bool]])->int:
	n=0
	for y in ra(8):#glyph bits
		for x in ra(8):
			i= r[y][x]
			i= int(not not i)
			n|= i<<(x+y*8)
	return n

@immut
class rune:
	names: list[str]
	gph: glyph
	def __post_init__(self):
		ass(type(self.gph),glyph)
		def a(k):
			if k==0:
				return
			if k in dic:
				pass#warn(f'runedic overwrite{k}')
			dic[k]= self
		a(self.gph.bin)
		for n in self.names:
			a(n)
			setattr(lib,n,self)

	def __str__(self):
		return f'{self.names}\n{self.gph}'

dic['empty']= rune('empty',glyph(0))

def strnrm(pile:list[str,rune]):
	ret=[]
	for e in pile:
		if type(e)==rune:
			ret+= [e]
		elif type(e)==str:
			if e not in dic:
				if type(e)==str:
					ret+= strnrm(list(e))
				continue
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
		b= rastint(g.raster)
		rune(g.names,glyph(b))

load_font('./font/lunatic.rmf')

class tests:
	#import atom

	def font():
		import space
		i=0
		l= dic.keys()
		#l= tuple( {e[0]:None for e in dic.values()}.keys() )#ordered dup eliminate
		#fixme lol

		W= 12
		ll= len(l)
		for e in l:
			p= ivec2(i%W,i//W)
			if   type(e)==str:
				space.body_s( p, e)
			elif type(e)==int:
				space.body(   p, glyph(e))
			i+= 1

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
			names= filter(lambda n: len(n)>1, r.names)
			s= ','.join(names)
			for x_,c in en(s):
				space.body(ivec2(x_+x+2,y),dic[c])

			#atom.text(s,ivec2(x+2,y))
			i+=1
