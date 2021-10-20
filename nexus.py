#nexus is the entry point which handles io and updates

from com import *
import pygame
import pygame.key
from pygame.locals import *
import time


import gl_backend
import rune
import space
if audio_enable:
	import audio
else:
	global audio
	audio= None
mods= [
	gl_backend,
	rune,
	space,
	audio,
]

#ioplexing
import pygame

class inplex:
	def key(bool_updown, keycode):pass#mouse buttons considered keys
	def mouse(ivec2):pass
class inplex_mapped(inplex):
	pass

for m in mods:
	if hasattr(m,'ioplex'):
		m.ioplex.keydown()


symbols=[
	'f00',
	'f01',
	'f02',
	'f10',
	'f11',
	'f12',
	'f20',
	'f21',
	'f22',
	'nl0',
	'nl1',
	'nl2',
	'nl3',
	'd00',
	'd01',
	'd02',
	'd10',
	'd11',
	'd12',
	'd20',
	'd21',
	'd22',
	'nr0',
	'nr1',
	'nr2',
	'nr3',
]
l=locals()
for s in symbols:
	l[s]=s
del l

#scancode->symbol
kbinds={
	  8:f00,
	 26:f01,
	 20:f02,
	  7:f10,
	 22:f11,
	  4:f12,
	  6:f20,
	 27:f21,
	 29:f22,
	 44:nl0,
	226:nl1,
	225:nl2,
	 57:nl3,
	 95:d00,
	 96:d01,
	 97:d02,
	 92:d10,
	 93:d11,
	 94:d12,
	 89:d20,
	 90:d21,
	 91:d22,
	 98:nr0,
	 99:nr1,
	 88:nr2,
	 87:nr3,
	}
frets={
	f00,
	f01,
	f02,
	f10,
	f11,
	f12,
	f20,
	f21,
	f22,
}
picks= set.difference(
	set(kbinds.values()),
		frets)

thr= lambda d: lambda b: space.thrust(b,d)

NoFret= object()
NoPick= object()
def kyes(i):
	if callable(i):
		return i()
	if i==None:
		return len(chord)==0
	if i==NoFret:
		return i not in frets
	if i==NoPick:
		return i not in picks
	else:
		return i in chord
ll= lambda a: [kyes(i) for i in a]
l_all= lambda *a: lambda : all(ll(a))
l_any= lambda *a: lambda : any(ll(a))

chord=[]#keys pressed currently
chords=[
	#condition  : effect
	#condition is a lambda which exaluates keys currently pressed against its construction here
	(l_all(l_any(NoFret,f00,f01,f02), d00 ),thr((-1, 1))),
	(l_all(l_any(NoFret,f00,f01,f02), d01 ),thr(( 0, 1))),
	(l_all(l_any(NoFret,f00,f01,f02), d02 ),thr(( 1, 1))),
	(l_all(l_any(NoFret,f00,f01,f02), d10 ),thr((-1, 0))),
	(l_all(l_any(NoFret,f00,f01,f02), d11 ),thr(( 0, 0))),
	(l_all(l_any(NoFret,f00,f01,f02), d12 ),thr(( 1, 0))),
	(l_all(l_any(NoFret,f00,f01,f02), d20 ),thr((-1,-1))),
	(l_all(l_any(NoFret,f00,f01,f02), d21 ),thr(( 0,-1))),
	(l_all(l_any(NoFret,f00,f01,f02), d22 ),thr(( 1,-1))),
]
effects={
	f00:space.w0,
	f01:space.w1,
	f02:space.w2,
}


def keychg(b,s):
	global chord
	if s not in kbinds:
		return
	k= kbinds[s]

	if audio:
		audio.note(b,symbols.index(k))

	if b:
		chord.append(k)

	for ci in chords:
		if ci[0]():
			ci[1](b)

	if not b:#after chord scan so that keyup still generates events
		chord.remove(k)

	if k in effects:
		effects[k](b)

def bind_remap():
	acc= {}
	global kbinds

	def g():
		while 1:
			for e in pygame.event.get():
				if e.type==KEYDOWN:
					yield e.scancode
	g=g()
	i=lambda: next(g)
	for b in kbinds.values():
		print(b[0]+':')
		s=i()
		print(s)
		acc.add(s,b)
	kbinds= acc
	del acc
def bindhelp(b):
	pass#todo discriptor display

if audio:
	audio.start()

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

				if e.key==K_F1:
					bindhelp(isdown)

				sc= e.scancode
				if sc in kbinds:
					keychg(isdown,sc)
			change=1
		#if change:pass#!!
		change=0


		#rune test
		if 1:
			i=0
			for y in ra(-16,16):
				for x in ra(-16,16):
					gl_backend.rune(x*2,y*2,0,int(1.05**i)&(0xFFFFFFFFFFFFFFFF))
					i+=1

		for m in mods:
			if hasattr(m,'step'):
				m.step()
			if hasattr(m,'render'):
				m.render()
		gl_backend.invoke()
		time.sleep(1./60.)
loop()

exit()