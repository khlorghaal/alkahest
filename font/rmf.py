import os.path
'''
raster monospaced font

eliminates the bulky metadata of normal font formats
and allows editing fonts with any text manipulator
does not require any over-specified and opaque GUI

made to export to bdf
currently no font renderers support rmf directly



each glyph is simply a line with the character,
followed by a plaintext raster of the character
any character may be used for solid color
'.' and ' ' are transparent

the width and heigh of the glyphs is specified only once
all rasters must conform to these dimensions

character names and codepoints are omitted entirely
as the characters encoded in the file can be used
to retrieve this data from specifications

header is very assertive/strict/aggressive,
must be in the exact format

RMF
W int
H int
AUTHOR str
LICENSE str
COMMENT str
_

example

RMF
W 7
H 7
AUTHOR khlorghaal
LICENSE WTFPL
COMMENT special characters full width, alphabetical w-1, lowercase w-1 h-1, numerical w-2, bracket interior padded
_

underscore required as last line of header
strings may be empty

font name is inferred from file name
'''
TODO= None#fixme wtf does this mean

from dataclasses import dataclass as dcls
@dcls
class glyph:
	char:chr#optional
	name:str#optional
	#one of char or name must be
	raster:tuple#((0|1),...)
	def print(self):
		for l in self.raster:
			print(''.join(map(str,l)))
		print()
class font:
	def __init__(self, char_wh):
		self.wh= char_wh
		assert(0<self.wh[1]<2048)
		assert(0<self.wh[0]<2048)
		self.glyphs={}

	#append glyphs into font, with empty rasters
	def init_empty(glyphs):
		for k in glyphs:
			g= glyphs[k]
			present= [g.char==g_.char for g_ in self.glyphs].contains(True)
			#^ meh?
			if present:
				print('glyph \'{}\' already present',g)
			else:
				TODO

	def print_chars(self,space=False):
		a= ''
		for (ch,g) in self.glyphs.items():
			a+= ch+(' ' if space else '')
		print(a)

	def save(self,fname):
		validate()
		TODO

	#gen_variants will generate [bold, italic][1x,2x,3x,4x]
	def save_bdf(self,fname,gen_variants=False):
		import bdflib
		from bdflib import model
		from bdflib import writer
		self.validate()
		name= os.path.splitext(fname)[0].encode('utf-8')
		bdf= bdflib.model.Font(name,1,700,800)
		for (ch,g) in self.glyphs.items():
			#bdflib *must* take an array of string-ints
			#because god is a lie
			rast= g.raster[::-1]#y axis flip
			#this trash converts the raster into
			rast= [ ['1' if c=='x' else '0' for c in r] for r in rast]
			#chars of 0|1
			rast= [ ''.join(r) for r in rast]
			print(rast)
			#merge the chars into a line
			rast= [ int(r,2)*2 for r in rast] #*2 because ??????
			#each line is string-parsed radix2 into int
			rast= [ b'%02x'%r for r in rast]
			#then converted back to a hex string
			print(ch)
			print(rast)
			bdf.new_glyph_from_data(
				name= bytes(ch,'utf-8'),
				data= rast,
				bbX=-3,
				bbY=0,
				bbW=self.wh[0],
				bbH=self.wh[1],
				advance= 0,
				codepoint= ord(ch))
		bdflib.writer.write_bdf(bdf, open(fname,'wb'))




def load(fname):
	with open(fname,'r') as f:
		lines= f.read().split('\n')

		#header, aggro
		assert(lines[0]=='RMF')
		assert(lines[1][:1:]=='W')
		assert(lines[2][:1:]=='H')
		w= int(lines[1][2:])
		h= int(lines[2][2:])
		assert(lines[3][:6]=='AUTHOR')
		assert(lines[4][:7]=='LICENSE')
		author=  lines[3][7:]
		license= lines[4][8:]
		assert(lines[5][:7]=='COMMENT')
		assert(lines[6]=='_')
		begin= 8-1#line of first glyph

		f= font((w,h))

		stride= h+1 #raster h + char identifier
		for line_num in range(begin,len(lines))[::stride]:
			def warn(s):
				print('warn: L:{:<5} {}'.format(line_num+1,s))# +1 because evil 1-indexing on files
			datum= lines[line_num:line_num+stride]
			meta= datum[0].split(' ')
			if len(meta)==0:
				warn('glyph has no char or name')
				continue
			m0= meta[0]
			tll= None
			if len(m0)<=1:#first tok is char
				if len(m0)==0:
					if m0=='':
						warn('glyph malf meta, line empty or leading whitespace')
					else:
						warn('glyph malf meta, first token malf %s'%meta)
					continue
				tll= 2
				assert(len(m0)==1)
				char= meta[0]
				name= meta[1] if len(meta)>=2 else None #name optional with char present
			else:#first tok is name
				char= None
				name= m0
				tll= 1

			if len(meta)>tll:
				warn('glyph notif, metadata trailing tokens ignored')

			if f.glyphs.get(char) is not None:
				warn('glyph warn, character is already assigned')
			if f.glyphs.get(name) is not None:
				warn('glyph warn, name is already assigned')
			#these both will replace the first

			rast= datum[1::]
			if(len(rast)!=h): warn('malf raster \n%s'%rast)
			for l in rast:
				if(len(l)!=w):
					warn('malf raster line \n%s'%l)
			#L= lambda c: ' ' if c=='.' or c==' ' else 'x'
			L= lambda c: 0 if c=='.' or c==' ' else 1
			rast= [[L(c) for c in l] for l in rast]
			rast= rast[::-1]#y axis flip
			rast= tuple(tuple(l) for l in rast)

			k= char or name
			f.glyphs[k]= glyph(char,name,rast)


	for (ch,g) in f.glyphs.items():
		#todo LALR validation 
		assert(g.char!=None or g.name!=None)
		if g.char!=None:
			assert(len(g.char)==1)
		assert(len(g.raster)==f.wh[1])
		for row in g.raster:
			assert(len(row )==f.wh[0])
		#todo move this to loading
		return f

