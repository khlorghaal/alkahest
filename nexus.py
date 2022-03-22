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
	 44:'nl0',226:'nl1',225:'nl2', 57:'nl3',	           98:'nr0', 99:'nr1', 88:'nr2'
	}
l=locals()
for scn,sym in kbinds.items():
	l[sym]=sym
del l

frets= {
	f33,f32,f31,f30,
	f23,f22,f21,f20,
	f13,f12,f11,f10,
	f03,f02,f01,f00,
	nl0,nl1,nl2,nl3
}
picks= frets - {kbinds.values()}

chord= set()#keys pressed currently

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
	chord: list[str]
	fun: callable

sputmul= lambda: 1<<(2*len(chord&{f00,f01,f02,f03}))
sput= lambda *d: lambda: space.thrust(ivec2(*d)*sputmul())

spem= lambda c:  lambda: space.emplace(c)

notes=(
	#pick:(frets,effect)

	#kinetic
	#cursor
	(d00,_any(nofr,f00,f01,f02,f03), sput(-1, 1)),
	(d01,_any(nofr,f00,f01,f02,f03), sput( 0, 1)),
	(d02,_any(nofr,f00,f01,f02,f03), sput( 1, 1)),
	(d10,_any(nofr,f00,f01,f02,f03), sput(-1, 0)),
	(d12,_any(nofr,f00,f01,f02,f03), sput( 1, 0)),
	(d20,_any(nofr,f00,f01,f02,f03), sput(-1,-1)),
	(d21,_any(nofr,f00,f01,f02,f03), sput( 0,-1)),
	(d22,_any(nofr,f00,f01,f02,f03), sput( 1,-1)),
	#zoom
	(nr0,_any(f00,f01,f02,f03), lambda: gl_backend.zoom(-1+len(chord&{f00,f01,f02,f03}))),

	(d11,nl0, lambda: space.aktivat(ROOT)),

	#arithmetic
	(nr0,_all(f10), spem('add' )),
	(nr0,_all(f11), spem('mul' )),
	(nr0,_all(f12), spem('pow' )),
	(nr0,_all(f13), spem('mod' )),
	(nr2,_all(f10), spem('len' )),
	(nr2,_all(f11), spem('nrm' )),
	(nr3,_all(f11), spem('grad')),
	(nr3,_all(f11), spem('dvrg')),
	(nr3,_all(f11), spem('flux')),
	#inverses
	(nr0,_all(f10,nl0),spem('sub' )),
	(nr0,_all(f11,nl0),spem('div' )),
	(nr0,_all(f12,nl0),spem('log' )),

	#morphic
)
'''

def key(k,ch,sc):
	global focus
	if focus.rune and focus.rune==rune.lib.text:
		focus.yeah

'''
def kchui():
	layout= [
		[f03, f02, f01, f00, 0, d00, d01, d02,   0],
		[f13, f12, f11, f10, 0, d10, d11, d12,   0],
		[f23, f22, f21, f20, 0, d20, d21, d22,   0],
		[nl3, nl2, nl1, nl0, 0, nr0, nr1, nr2, nr3]
		]
	for y,r in en(layout[::-1]):
		for x,l in en(r):
			if l==0:
				continue
			m= space.mod.none if l in chord else space.mod.c
			space.body(ivec2(x,y),rune.dic.border,z=-1,mod=m)





class ROOT:
	def inp(b,ch,sc):
		if sc not in kbinds:
			return False
		k= kbinds[sc]

		if k in frets:
			if b:
				chord.add(k)
			else:
				chord.remove(k)
		else:
			p=k
			if b:
				for n in notes:
					if n[0]!=p:
						continue
					if n[1]():
						if audio:#todo actual frets
							audio.chord(chord)
						n[2]()
						


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
				if e.button==4:#wheel
					gl_backend.zoomin()
				if e.button==5:#wheel
					gl_backend.zoomou()
			if e.type==KEYDOWN or e.type==KEYUP:
				isdown= e.type==KEYDOWN

				k=e.key
				if k==K_F1:
					bindhelp(isdown)

				ch= e.unicode
				sc= e.scancode

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
			gl_backend.invoke()

		time.sleep(1./60.)
loop()

#space.save()

exit()
	