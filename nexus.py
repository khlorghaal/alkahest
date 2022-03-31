#nexus is the entry point
#	handles OS intercho, io, updates
#logic here should be kept minimal and moved into modules as needed

from com import *
import pygame
import pygame.key
from pygame.locals import *
import time


import rune
import space
import atom
import gl_backend
if audio_enable:
	import audio
else:
	global audio
	audio= None

#scancode->symbol
kbinds={
	 30:'f33', 31:'f32', 32:'f31', 33:'f30',               84:'nr6', 85:'nr5', 86:'nr4',
	 20:'f23', 26:'f22',  8:'f21', 21:'f20',	 89:'d20', 90:'d21', 91:'d22', 
	  4:'f13', 22:'f12',  7:'f11',  9:'f10',	 92:'d10', 93:'d11', 94:'d12', 87:'nr3',
	 29:'f03', 27:'f02',  6:'f01', 25:'f00',	 95:'d00', 96:'d01', 97:'d02', 

	53: 'fb5',43:'fb4', 225:'fb3',224:'fb2', 226:'fb1',44:'fb0',	           98:'nr0', 99:'nr1', 88:'nr2'
	}
for sym in kbinds.values():
	locals()[sym]=sym
key_layout= [
	[fb5, f33, f32, f31, f30,   0, 0,   0, nr6, nr5, nr4],
	[fb4, f23, f22, f21, f20,   0, 0, d00, d01, d02, nr3],
	[  0, f13, f12, f11, f10,   0, 0, d10, d11, d12, nr3],
	[fb3, f03, f02, f01, f00,   0, 0, d20, d21, d22, nr2],
	[fb2,   0, fb1, fb0, fb0, fb0, 0, nr0, nr0, nr1, nr2]
]

frets= (
	f33,f32,f31,f30,
	f23,f22,f21,f20,
	f13,f12,f11,f10,
	f03,f02,f01,f00,
	fb0,fb1,fb2,fb3,fb4,fb5
)

fstate= set()#frets only
kstate= set()#any bound keys

_may= lambda ch: lambda:     not fstate or  fstate.issubset(ch)
_any= lambda ch: lambda: not not fstate and fstate.issubset(ch)
_all= lambda ch: lambda: fstate==ch
_non= lambda ch: lambda: not fstate

@dcls
class cho:
	pick: str
	fret_eval: callable
	row: int
	frets: tuple[str]
	fun: callable
	tags: list[str]#for user searches

	def __post_init__(s):
		s.fret_eval= s.fret_eval(s.frets)#collapse outer lambda

sputmul= lambda: 1<<(2*len(fstate&{f00,f01,f02,f03}))
sput= lambda *d: lambda: space.thrust(ivec2(*d)*sputmul())
spem= lambda c:  lambda: space.emplace(c)
def zch():
	space.cursor.prime.z= len(fstate&{f00,f01,f02,f03})
rch= lambda s: rune.dic[s]

chords= [cho(*c) for c in [
	#pick:(frets,effect)
	#commas on single element are necessary to form tuples

	#kinetic
	#cursor
	(d00,_may,0,{f00,f01,f02,f03}, sput(-1, 1),['north left']),
	(d01,_may,0,{f00,f01,f02,f03}, sput( 0, 1),['up']),
	(d02,_may,0,{f00,f01,f02,f03}, sput( 1, 1),['north right']),
	(d10,_may,0,{f00,f01,f02,f03}, sput(-1, 0),['west']),
	(d12,_may,0,{f00,f01,f02,f03}, sput( 1, 0),['east']),
	(d20,_may,0,{f00,f01,f02,f03}, sput(-1,-1),['south left']),
	(d21,_may,0,{f00,f01,f02,f03}, sput( 0,-1),['down']),
	(d22,_may,0,{f00,f01,f02,f03}, sput( 1,-1),['south right']),
	#zoom
	(d11,_may,0,(f00,f01,f02,f03), zch,['zoom']),

	(d11,_all,0,(fb1,), lambda: space.aktivat(ROOT),['focus']),

	#arithmetic
	(nr0,_all,1,{f10,   },spem('add' ),[rch('add' ),' add' ]),
	(nr0,_all,1,{f10,fb0},spem('sub' ),[rch('sub' ),' sub' ]),
	(nr0,_all,1,{f11,   },spem('mul' ),[rch('mul' ),' mul' ]),
	(nr0,_all,1,{f11,fb0},spem('div' ),[rch('div' ),' div' ]),
	(nr0,_all,1,{f12,   },spem('pow' ),[rch('pow' ),' pow' ]),
	(nr0,_all,1,{f12,fb0},spem('log' ),[rch('log' ),' log' ]),
	(nr0,_all,1,{f13,   },spem('mod' ),[rch('mod' ),' mod' ]),
	(nr2,_all,1,{f10,   },spem('len' ),[rch('len' ),' len' ]),
	(nr2,_all,1,{f11,   },spem('nrm' ),[rch('nrm' ),' nrm' ]),
	(nr3,_all,1,{f10,   },spem('grad'),[rch('grad'),' grad']),
	(nr3,_all,1,{f11,   },spem('dvrg'),[rch('dvrg'),' dvrg']),
	(nr3,_all,1,{f12,   },spem('lapl'),[rch('lapl'),' lapl']),
	(nr3,_all,1,{f13,   },spem('flux'),[rch('flux'),' flux']),
	(nr4,_all,1,{f10,   },spem( 'fft'),[rch( 'fft'),'  fft']),
	(nr4,_all,1,{f10,fb0},spem('ifft'),[rch('ifft'),' ifft']),
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
	#bus
]]


def ui():
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
				space.body(ivec2(x,y)+1,r,z=-2)

		#chords available
		for y,cd in en(chords):
			p= cd.pick
			fr= [False]*4

			if cd.fret_eval():#full match
				m= space.mod.active#active
			elif _any(cd.frets)():#partial match
				m= space.mod.highlight#spicey
				if cd.fret_eval==_any:
					m= space.mod.active
			else:
				m= space.mod.none

			#mark static mask
			for x,f in en(frets[:16]):
				fr[x%4]|= f in cd.frets

			#prime fret
			for x,f in en(fr):
				#m= space.mod.h if ch in kstate else space.mod.none 
				r= square if f else box
				space.body(ivec2(x+1,y+6)+1,r,z=-2,mod=m)

			if len(cd.frets)>0:
				rp= rune.dic['measure_y%s'%(cd.row*2)]
			else:
				rp= rune.lib.nul
			s= [rp,' ',*cd.tags]
			for x,r in en(rune.strnrm(s)):
				m= space.mod.none
				space.body(ivec2(x+5,y+6)+1,r,z=-2,mod=m)




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

#space.load()
rune.tests()
#atom.tests()
#space.tests()

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
					p= space.cursor.prime.b.p
					z= 1<<space.cursor.prime.z
					w,h = pygame.display.get_surface().get_size()
					c= ivec2(*pygame.mouse.get_pos())
					c.x=   c.x -w//2
					c.y= h-c.y -h//2
					c+= 4*z
					c//= 8
					c//= z
					c+= p
					print(c)
					space.cursor.prime.place(c)
				if e.button==4:#wheel
					space.cursor.prime.zoom( 1)
				if e.button==5:#wheel
					space.cursor.prime.zoom(-1)
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
		change|= space.step()!=None
		if change or RENDER_ALWAYS:
			change=0
			ui()
			gl_backend.invoke()

		time.sleep(1./60.)
loop()

#space.save()

exit()