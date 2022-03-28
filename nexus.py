#nexus is the entry point
#	handles OS interop, io, updates
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
l=locals()
for scn,sym in kbinds.items():
	l[sym]=sym
del l
key_layout= [
	[fb5, f33, f32, f31, f30,   0, 0,   0, nr6, nr5, nr4],
	[fb4, f23, f22, f21, f20,   0, 0, d00, d01, d02, nr3],
	[  0, f13, f12, f11, f10,   0, 0, d10, d11, d12, nr3],
	[fb3, f03, f02, f01, f00,   0, 0, d20, d21, d22, nr2],
	[fb2,   0, fb1, fb0, fb0, fb0, 0, nr0, nr1,   0, nr2]
]

frets= {
	f33,f32,f31,f30,
	f23,f22,f21,f20,
	f13,f12,f11,f10,
	f03,f02,f01,f00,
	fb0,fb1,fb2,fb3,fb4,fb5
}
picks= frets - {kbinds.values()}

chord= set()#keys pressed currently
kstate= set()

NoFret= nofr= object()
def kyes(i):
	if callable(i):#subclauses
		return i()
	if i==NoFret:
		return i not in frets
	else:
		return i in chord
ll= lambda a: [kyes(i) for i in a]
_all= lambda *a: lambda: all(ll(a))
_any= lambda *a: lambda: any(ll(a))

@dcls
class op:
	pick: str
	fret_pass: callable
	frets: tuple[str]
	fun: callable
	tags= tuple[str]#for searching

sputmul= lambda: 1<<(2*len(chord&{f00,f01,f02,f03}))
sput= lambda *d: lambda: space.thrust(ivec2(*d)*sputmul())
spem= lambda c:  lambda: space.emplace(c)
def zch():
	space.cursor.prime.z= -1+len(chord&{f00,f01,f02,f03})

chords=(
	#pick:(frets,effect)

	#kinetic
	#cursor
	op(d00,_any,(nofr,f00,f01,f02,f03), sput(-1, 1)),
	op(d01,_any,(nofr,f00,f01,f02,f03), sput( 0, 1)),
	op(d02,_any,(nofr,f00,f01,f02,f03), sput( 1, 1)),
	op(d10,_any,(nofr,f00,f01,f02,f03), sput(-1, 0)),
	op(d12,_any,(nofr,f00,f01,f02,f03), sput( 1, 0)),
	op(d20,_any,(nofr,f00,f01,f02,f03), sput(-1,-1)),
	op(d21,_any,(nofr,f00,f01,f02,f03), sput( 0,-1)),
	op(d22,_any,(nofr,f00,f01,f02,f03), sput( 1,-1)),
	#zoom
	op(nr0,_any,(f00,f01,f02,f03), zch),

	op(d11,_any,(fb0), lambda: space.aktivat(ROOT)),

	#arithmetic
	op(nr0,_all,(f10    ),spem('add' )),
	op(nr0,_all,(f10,fb0),spem('sub' )),
	op(nr0,_all,(f11    ),spem('mul' )),
	op(nr0,_all,(f11,fb0),spem('div' )),
	op(nr0,_all,(f12    ),spem('pow' )),
	op(nr0,_all,(f12,fb0),spem('log' )),
	op(nr0,_all,(f13    ),spem('mod' )),
	op(nr2,_all,(f10    ),spem('len' )),
	op(nr2,_all,(f11    ),spem('nrm' )),
	op(nr3,_all,(f11    ),spem('grad')),
	op(nr3,_all,(f11    ),spem('dvrg')),
	op(nr3,_all,(f11    ),spem('flux')),
	op(nr4,_all,(f10    ),spem( 'fft')),
	op(nr4,_all,(f10,fb0),spem('ifft')),
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
)


def kchui():
	for y,r in en(key_layout[::-1]):
		for x,c in en(r):
			if c==0:
				continue
			on= c in kstate
			m= space.mod.h if on else space.mod.none
			r= rune.lib.border if on else rune.lib.square
			space.body(ivec2(x,y)+1,r,z=-1,mod=m)





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
				chord.add(k)
			else:
				chord.remove(k)
		else:
			p=k
			if b:
				for n in chords:#opt
					if n.pick!=p:
						continue
					if n.fret_pass(n.frets):
						if audio:#todo actual frets
							audio.chord(chord)
						n.fun()
						


	def bind_remap():
		acc= {}
		global kbinds

		def g():
			while 1:
				for e in pygame.event.get():
					if e.type==KEYDOWN:
						yield e.scancode
		g=g()
		for b in kbinds.values():
			print(b[0]+':')
			s=next(g)
			acc.add(s,b)
		kbinds= acc
		del acc
	def bindhelp(b):
		pass#todo

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
			kchui()
			gl_backend.invoke()

		time.sleep(1./60.)
loop()

#space.save()

exit()