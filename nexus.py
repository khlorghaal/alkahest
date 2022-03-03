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
import pygame


symbols=[
	'f00','f01','f02',
	'f10','f11','f12',
	'f20','f21','f22',
	'nl0','nl1','nl2','nl3',
	'd00','d01','d02',
	'd10','d11','d12',
	'd20','d21','d22',
	'nr0','nr1','nr2','nr3',
]
l=locals()
for s in symbols:
	l[s]=s
del l

#scancode->symbol
kbinds={
	  8:f00, 26:f01, 20:f02,
	  7:f10, 22:f11,  4:f12,
	  6:f20, 27:f21, 29:f22,
	 44:nl0,226:nl1,225:nl2, 57:nl3,
	 95:d00, 96:d01, 97:d02,
	 92:d10, 93:d11, 94:d12,
	 89:d20, 90:d21, 91:d22,
	 98:nr0, 99:nr1, 88:nr2, 87:nr3,
	}
frets={
	f00,f01,f02,
	f10,f11,f12,
	f20,f21,f22,
}
picks= set.difference(
	set(kbinds.values()),
		frets)

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

onhit= lambda l: lambda b: l() if b else  () 
onrel= lambda l: lambda b:  () if b else l() 

chord=[]#keys pressed currently
chords=[
	#(condition,effect)
	#condition is a lambda which evaluates keys currently pressed against its construction here
	*[
		(
			l_all(l_any(NoFret,f00,f01,f02), k ),
			lambda b,d=d: space.thrust(b,ivec2(*d))
		) for k,d in [
			(d00,(-1, 1)),
			(d01,( 0, 1)),
			(d02,( 1, 1)),
			(d10,(-1, 0)),
			(d12,( 1, 0)),
			(d20,(-1,-1)),
			(d21,( 0,-1)),
			(d22,( 1,-1))
		]
	],
	*[
		(
			l_all(f,n),
			onhit(lambda c=c: space.emplace(c))
		) for f,n,c in [
			(f10,nr0,'+'),
			(f11,nr0,'*'),
			(f12,nr0,'^'),
			(f10,nr1,'-'),
			(f11,nr1,'div'),
			(f12,nr1,'log'),
		]
	],
	(l_all(d11),onhit(space.aktivat)),
	(l_any(f00), space.wset(0)),
	(l_any(f01), space.wset(1)),
	(l_any(f02), space.wset(2))
]
'''

def key(k,ch,sc):
	global focus
	if focus.rune and focus.rune==rune.lib.text:
		focus.yeah

'''


class ROOT:
	def inp(b,ch,sc):
		if sc not in kbinds:
			return False
		k= kbinds[sc]

		if audio:
			audio.note(b,symbols.index(k))
			#todo actual frets

		if b:
			chord.append(k)

		for ci in chords:
			if ci[0]():
				ci[1](b)

		if not b:#after chord scan so that keyup still generates events
			chord.remove(k)

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
			print(s)
			acc.add(s,b)
		kbinds= acc
		del acc
	def bindhelp(b):
		pass#todo discriptor display

focus(ROOT)

if audio:
	audio.start()

rune.tests()
#atom.tests()

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

				#chars pygame likent
				if len(ch)!=0:
					ochd={
						32:' ',
						13:'\n'
						}
					och= ord(ch)
					print(och)
					if och in ochd:
						ch= ochd[och]

				focus().inp(isdown,ch,sc)

			change=1
		change|= space.step()!=None
		if change:
			change=0
			gl_backend.invoke()

		time.sleep(1./60.)
loop()

exit()
