import gl_backend

import pygame
import pygame.key
import time
from pygame.locals import *
from numpy import *
ra= range
en= enumerate

kmap= {
	K_LEFT: (-1, 0),
	K_RIGHT:( 1, 0),
	K_UP:   ( 0, 1),
	K_DOWN: ( 0,-1)
}

ori=[[1]]
class cur:
	rast=[
		[1,1,1],
		[1,0,1],
		[1,1,1],
	]
	pos= array((0,0))
	vel= array((0,0))
	vel_active=0

def render():
	gl_backend.quad((0,0,0))
	for j in ra(-4,5):
		for i in ra(-4,5):
			gl_backend.quad((i*2,j*2,0))

	gl_backend.quad((*cur.pos,0))
	#gl_backend.blit(cur.rast,cur.pos)
	gl_backend.invoke(8)


def loop():
	while(1):
		#input
		for e in pygame.event.get():
			if e.type==MOUSEMOTION:
				continue
			if e.type==MOUSEBUTTONDOWN:
				if e.button==4:#wheel
					gl_backend.zoomin()
				if e.button==5:#wheel
					gl_backend.zoomou()
			if e.type==TEXTINPUT:
				continue
			if (e.type == QUIT) or (e.type == KEYUP and e.key == K_ESCAPE):
				pygame.quit()
				return
			if e.type==KEYDOWN:
				k= e.key
				if k in kmap:
					d= kmap[k]
					cur.vel+= d
					if ~cur.vel_active:
						cur.pos+= d
						gl_backend.tr= cur.pos
			if e.type==KEYUP:
				if k in kmap:
					d= kmap[k]
					cur.vel-= d

		#motion
		if cur.vel_active:
			cur.pos+= cur.vel
			gl_backend.tr= cur.pos
		render()
		time.sleep(1./30.)
loop()