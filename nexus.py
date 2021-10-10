import com
import pygame
import pygame.key
import time
from pygame.locals import *

import importlib

mods= [
	#'rune',
	'space',
	'gl_backend',
]
mods= {m: importlib.import_module(m) for m in mods}

gl_backend= mods['gl_backend']

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

from space import thrust
kmap= {
	K_LEFT: lambda d: thrust(d,(-1, 0)),
	K_RIGHT:lambda d: thrust(d,( 1, 0)),
	K_UP:   lambda d: thrust(d,( 0, 1)),
	K_DOWN: lambda d: thrust(d,( 0,-1))
}

def loop():
	while(1):
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
				k= e.key
				up= e.type==KEYUP
				if k in kmap:
					kmap[k](up)
			change=1
		#if change:pass#!!
		change=0

		for m in mods:
			if hasattr(m,'step'):
				m.step()
			if hasattr(m,'render'):
				m.render()
		gl_backend.invoke()
		time.sleep(1./30.)
loop()