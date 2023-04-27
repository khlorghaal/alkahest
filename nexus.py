'''
nexus is the entry point
	handles
		platform multiplex (OS)
		io, keybinding
		macroscale control flow
logic here should be kept minimal and moved into modules as needed

todo all inputs must be converted into atomic runes

contexts
	the context is the currently routed input reciever
	-cursor: the root context
		escape always returns control to the cursor
		nesting of contexts is probably not.
	-text: traditional textbox allowing typing
		characters converted into runes within a bound
		bound expands dynamically as able without overwriting neighbors
		multichars also supported via [multichar bind]
	-raster:
		visually similar to a display but very different
		each px of the raster is a glyph for on|off
		abstract class
		-subclass glyphraster
			8x8 strictly
			can be invoked upon any glyph
				this materializes a z=2 bound
			submitted glyph checked for rune match
			-subclass runeraster
				font editing
				application is global
				all glyphs matching old rune updated to new rune

				todo
				howto new a rune?
				should be a program
					what even is a program?
				will be ignored since text based editor is fine

	
'''

import sys
from IPython.core import ultratb
sys.excepthook = ultratb.FormattedTB(mode='Plain', color_scheme='Linux', call_pdb=False)

from com import *
import pygame
import pygame.key
from pygame.locals import *
import time


import rune
import space
import atom
import gl_backend
import transpiler
if audio_enable:
	import audio
else:
	global audio
	audio= None

#scancode->symbol
kbinds={
	 30:'f33', 31:'f32', 32:'f31', 33:'f30',               84:'pk6', 85:'pk5', 86:'pk4',
	 20:'f23', 26:'f22',  8:'f21', 21:'f20',	 89:'d20', 90:'d21', 91:'d22', 
	  4:'f13', 22:'f12',  7:'f11',  9:'f10',	 92:'d10', 93:'d11', 94:'d12', 87:'pk3',
	 29:'f03', 27:'f02',  6:'f01', 25:'f00',	 95:'d00', 96:'d01', 97:'d02', 

	53: 'bf5',43:'bf4', 225:'bf3',224:'bf2', 226:'bf1',44:'bf0',	           98:'pk0', 99:'pk1', 88:'pk2'
	}
for sym in kbinds.values():
	locals()[sym]=sym
key_layout= [
	[bf5, f33, f32, f31, f30,   0, 0,   0, pk6, pk5, pk4],
	[bf4, f23, f22, f21, f20,   0, 0, d00, d01, d02, pk3],
	[  0, f13, f12, f11, f10,   0, 0, d10, d11, d12, pk3],
	[bf3, f03, f02, f01, f00,   0, 0, d20, d21, d22, pk2],
	[bf2,   0, bf1, bf0, bf0, bf0, 0, pk0, pk0, pk1, pk2]
]

frets= (
	f33,f32,f31,f30,
	f23,f22,f21,f20,
	f13,f12,f11,f10,
	f03,f02,f01,f00,
	bf0,bf1,bf2,bf3,bf4,bf5
)
frets_lower={
	bf0,bf1,bf2,bf3,bf4,bf5
}

fstate= set()#frets only
kstate= set()#any bound keys

_may= lambda ch: lambda:     not fstate or  fstate.issubset(ch)
_any= lambda ch: lambda: not not fstate and fstate.issubset(ch)
_all= lambda ch: lambda: fstate==ch
_non= lambda ch: lambda: not fstate

@dcls
class cho:
	fret_eval: callable
	frets: set[str]
	pick: str
	fun: callable
	tags: list[str]#for user searches
	fret_eval_eval: callable= None #pre lambda collapse

	def __post_init__(s):
		s.fret_eval_eval= s.fret_eval#woe
		s.fret_eval= s.fret_eval(s.frets)#collapse outer lambda

sputmul= lambda: 1<<(2*len(fstate&{f00,f01,f02,f03}))
sput= lambda *d: lambda: atom.cursor.thrust(ivec2(*d)*sputmul())
spem= lambda c:  lambda: atom.cursor.prime.emits(c)
def zch():
	atom.cursor.prime.zoom= len(fstate&{f00,f01,f02,f03})
rch= lambda s: rune.dic[s]

chords= [cho(*c) for c in [
	#pick:(frets,effect)
	#commas on single element are necessary to form tuples

	#(_all,{bf2},pk0,space.search_emplace,['search emplace']),

	#kinetic
	#cursor
	(_may,{f00,f01,f02,f03},d00, sput(-1, 1),['north left']),
	(_may,{f00,f01,f02,f03},d01, sput( 0, 1),['up']),
	(_may,{f00,f01,f02,f03},d02, sput( 1, 1),['north right']),
	(_may,{f00,f01,f02,f03},d10, sput(-1, 0),['west']),
	(_may,{f00,f01,f02,f03},d12, sput( 1, 0),['east']),
	(_may,{f00,f01,f02,f03},d20, sput(-1,-1),['south left']),
	(_may,{f00,f01,f02,f03},d21, sput( 0,-1),['down']),
	(_may,{f00,f01,f02,f03},d22, sput( 1,-1),['south right']),
	#zoom
	(_may,(f00,f01,f02,f03),d11, zch,['zoom']),

	(_all,(bf1,),d11, lambda: space.aktivat(ROOT),['focus']),
	(_all,(bf1,),d11, lambda: space.aktivat(ROOT),['focus']),

	#arithmetic
	(_all,{f10,   },pk0,spem('add' ),[rch('add' ),' add' ]),
	(_all,{f10,bf0},pk0,spem('sub' ),[rch('sub' ),' sub' ]),
	(_all,{f11,   },pk0,spem('mul' ),[rch('mul' ),' mul' ]),
	(_all,{f11,bf0},pk0,spem('div' ),[rch('div' ),' div' ]),
	(_all,{f12,   },pk0,spem('pow' ),[rch('pow' ),' pow' ]),
	(_all,{f12,bf0},pk0,spem('log' ),[rch('log' ),' log' ]),
	(_all,{f13,   },pk0,spem('mod' ),[rch('mod' ),' mod' ]),
	(_all,{f10,   },pk2,spem('len' ),[rch('len' ),' len' ]),
	(_all,{f11,   },pk2,spem('nrm' ),[rch('nrm' ),' nrm' ]),
	(_all,{f10,   },pk3,spem('grad'),[rch('grad'),' grad']),
	(_all,{f11,   },pk3,spem('dvrg'),[rch('dvrg'),' dvrg']),
	(_all,{f12,   },pk3,spem('lapl'),[rch('lapl'),' lapl']),
	(_all,{f13,   },pk3,spem('flux'),[rch('flux'),' flux']),
	(_all,{f10,   },pk4,spem( 'fft'),[rch( 'fft'),'  fft']),
	(_all,{f10,bf0},pk4,spem('ifft'),[rch('ifft'),' ifft']),
	#shr
	#shl
	#clz
	#ctz
	#and
	#or
	#xor
	#brd
	#bwr

	#morphic
	(_non,{},pk0,space.kill,['del' ]),
	(_all,{bf0},pk0,spem('bus'),[rch('bus'),' bus']),

	#systemic
#	(_all,{bf5},pk0,atom.word,['word']),
	#(_all,{bf2},pk0,atom.eval,['eval']),

	(_all,{bf5},pk4,space.load,['load']),
	(_all,{bf2},pk4,space.save,['save']),
]]


#screenspace glyphs
#internally stateless, used to display state
def hud():
	if focus()==ROOT:
		square= rune.lib.square
		box= rune.lib.box

		#keys pressed
		for y,r in en(key_layout[::-1]):
			for x,c in en(r):
				if c==0:
					continue
				on= c in kstate
				r= box if on else square
				space.body(ivec2(x,y)+1,r.gph,z=-1,align=ivec2(-1,-1))

		#chord index
		for y,cd in en(chords):
			p= cd.pick
			fr= [False]*4

			if cd.fret_eval():#full match
				m= space.mod.aktiv
			elif _any(cd.frets)():#partial match
				m= space.mod.highlight
				#if cd.fret_eval_eval==_any:
				#	m= space.mod.none
			else:
				m= space.mod.none

			if cd.fret_eval_eval in [_may,_non] and len(fstate)==0:
				m= space.mod.none

			x=0#print column
			def put(r, _m=None):
				nonlocal x
				if _m==None:
					nonlocal m
					assert(m!=None)
				r= r if type(r)==rune.rune else rune.dic[r]
				space.body_r(ivec2(x-6,y+6),r,mod=m,z=-1,align=ivec2(-1,-1))
				x+=1
			def puts(s):
				for r in rune.strnrm(s):
					put(r)

			#fret mask
			for x,f in en(frets[:4*4]): #fixme make 2d
				fr[x%4]|= f in cd.frets


			#prime fret
			for f in fr:
				_m= space.mod.h if f in kstate else space.mod.none 
				put('square' if f else 'box',_m)

			#lower fret
			_x=x
			for f in set(cd.frets)&frets_lower:
				puts(f)
			if _x==x:
				x+=3

			#pick labal
			puts(p)
			x+=1

			#tags labal
			s= [' ',*cd.tags]
			puts(s)




class ROOT:
	def inp(b,ch,sc):
		if sc not in kbinds:
			return False
		k= kbinds[sc]

		if b:
			kstate.add(k)
		else:
			kstate.remove(k)
		if k in frets:
			if b:
				fstate.add(k)
			else:
				fstate.remove(k)
		else:#is pick
			p=k
			if b:
				for n in chords:#chot
					if n.pick!=p:
						continue
					if n.fret_eval():
						if audio:#todo actual frets
							audio.chord(fstate)
						n.fun()
						
focus(ROOT)

if audio:
	audio.start()

space.load()
#atom.tests()
#transpiler.tests()
#space.tests()
#rune.tests.font()


RENDER_ALWAYS= True

def loop():
	while 1:
		change= 0

		#input
		for e in pygame.event.get():
			if (e.type == QUIT) or (e.type == KEYUP and e.key == K_ESCAPE):
				pygame.quit()
				return
			if e.type==MOUSEMOTION or e.type==TEXTINPUT:
				continue

			if e.type==MOUSEBUTTONDOWN:
				if e.button==1:#LMB
					#todo cleanup
					p= atom.cursor.prime.b.p
					z= 1<<atom.cursor.prime.zoom
					w,h = pygame.display.get_surface().get_size()
					c= ivec2(*pygame.mouse.get_pos())
					c.x=   c.x - w//2
					c.y= h-c.y - h//2
					c+= 4*z
					c//=8*z
					c+= p #relative to present, not origin
					print('cursor@%s'%c)
					atom.cursor.prime.move(c)
				if e.button==4:#wheel
					atom.cursor.prime.zoomd( 1)
				if e.button==5:#wheel
					atom.cursor.prime.zoomd(-1)
			if e.type==KEYDOWN or e.type==KEYUP:
				isdown= e.type==KEYDOWN

				k=e.key
				if k==K_F1:
					bindhelp(isdown)

				ch= e.unicode
				sc= e.scancode
				#print(sc)

				#pygame likent these chars
				ch={
					32:' ',
					13:'\n'
					}.get(ord(ch or ' ')) or ch

				focus().inp(isdown,ch,sc)

			change=1
		atom._loop()
		change|= atom.step()!=None
		if change or RENDER_ALWAYS:
			change=0
			hud()
			gl_backend.invoke()

		time.sleep(1./60.)
loop()

#space.save()

exit()