from com import *
import pygame
import pygame.key
from pygame.locals import *
import time

import importlib

mods= [
	'rune',
	'space',
	'gl_backend',
]#load order may not be ordered
mods= {m: importlib.import_module(m) for m in mods}
import gl_backend
import rune
import space

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


import space

#scancode->(name,lam)
kbinds= {
	  8:('f00',space.w0),
	 26:('f01',space.w1),
	 20:('f02',space.w2),
	  7:('f10',lambda _:None),
	 22:('f11',lambda _:None),
	  4:('f12',lambda _:None),
	  6:('f20',lambda _:None),
	 27:('f21',lambda _:None),
	 29:('f22',lambda _:None),
	 95:('d00',lambda b:space.thrust(b,(-1, 1))),
	 96:('d01',lambda b:space.thrust(b,( 0, 1))),
	 97:('d02',lambda b:space.thrust(b,( 1, 1))),
	 92:('d10',lambda b:space.thrust(b,(-1, 0))),
	 93:('d11',lambda _:None),
	 94:('d12',lambda b:space.thrust(b,( 1, 0))),
	 89:('d20',lambda b:space.thrust(b,(-1,-1))),
	 90:('d21',lambda b:space.thrust(b,( 0,-1))),
	 91:('d22',lambda b:space.thrust(b,( 1,-1))),
	 44:('sl0',lambda _:None),
	226:('sl1',lambda _:None),
	225:('sl2',lambda _:None),
	 57:('sl3',lambda _:None),
	 98:('sr0',lambda _:None),
	 99:('sr1',lambda _:None),
	 88:('sr2',lambda _:None),
	 87:('sr3',lambda _:None),
	}

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
				sc= e.scancode
				isdown= e.type==KEYDOWN
				if sc in kbinds:
					kbinds[sc][1](isdown)
			change=1
		#if change:pass#!!
		change=0


		#rune test
		if 1:#!!
			i=0
			for y in ra(-16,16):
				for x in ra(-16,16):
					gl_backend.rune(x*2,y*2,int(1.05**i)&(0xFFFFFFFFFFFFFFFF))
					i+=1

		for n in mods:
			m= mods[n]
			if hasattr(m,'step'):
				m.step()
			if hasattr(m,'render'):
				m.render()
		gl_backend.invoke()
		time.sleep(1./30.)
loop()