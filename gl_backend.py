from com import *

import rune
import space

import numpy as np
import png
#import exr

import pygame
from pygame.locals import *

import ctypes as ct
void_p= ct.c_void_p
from OpenGL.GL import *
from OpenGL.GL import shaders

import numpy


def setwh(_w,_h):
	global w
	global h
	w= _w
	h= _h
	global whmax
	global whmin
	whmax= max(w,h)
	whmin= min(w,h)
	glViewport(0,0,w,h)
setwh(*resolution)

zoomin= lambda:	zoom(z+1)
zoomou= lambda:	zoom(z-1)


pygame.init()
pygame.display.set_mode(resolution, DOUBLEBUF | OPENGL )
pygame.display.set_caption('____________________________')

import re
class prog:
	id= -1
	unis= {}
	ulocs= {}
	def bind(self):
		glUseProgram(self.id)
	def shex(e):
		print('\nSHADERROR\n')
		e= str(e)
		e= e.replace('\\\\n','\n')
		e= e.replace(  '\\n','\n')
		e= e.replace(  '\\t','\t')
		e= e.replace(  '\\t','\t')
		e= e.replace(  '\\','')
		e= e.replace('\\\\','')#fuck
		e= re.sub(r'\(([0-9]+)\)', r'\nFile " ", line \1', e)
		#sublime default error regex
		print(e)
		exit()
	def shpp(src,flags=[]):
		return '\n'.join([
			'#version 450',
			*['#define %s 1'%d for d in flags],
			open('shaderheaders/base.glsl').read(),
			'#line 1',
			src
		])
class prog_vf(prog):
	def __init__(self, vert,frag,flags=[]):
		super(prog,self).__init__()
		try:
			self.vert= prog.shpp(vert,flags)
			self.frag= prog.shpp(frag,flags)
			self.ivert= shaders.compileShader(self.vert, GL_VERTEX_SHADER)
			self.ifrag= shaders.compileShader(self.frag, GL_FRAGMENT_SHADER)
			self.id=   shaders.compileProgram(self.ivert,self.ifrag)
		except Exception as e:
			prog.shex(e)
class prog_c(prog):
	def __init__(self,src,flags=[]):
		super(prog,self).__init__()
		try:
			src_p= prog.shpp(src,flags)
			sh= shaders.compileShader(src_p, GL_COMPUTE_SHADER)
			self.id= shaders.compileProgram(sh)
		except Exception as e:
			prog.shex(e)





prog_rune= prog_vf('''
layout(location=0) uniform ivec4 tr;
layout(location=1) uniform vec2 res;
layout(location=2) uniform long tick;

layout(location=0) in ivec4 in_p;
layout(location=1) in uvec2 in_rune;
layout(location=2) in uint  in_mod;
smooth out vec2 vuv;//ints cant smooth
flat out uvec2 vrune;
flat out uint  vmod;
void main(){
	vmod= in_mod;

	const int W= 8;
	const int W2= W/2;
	const ivec2[] lxy= ivec2[](
		ivec2(-W2,-W2),
		ivec2(-W2, W2),
		ivec2( W2, W2),
		ivec2( W2,-W2)
	);
	const vec2[] luv= vec2[](
		ivec2( 0, 0),
		ivec2( 0, W),
		ivec2( W, W),
		ivec2( W, 0)
	);

	ivec2 xy= lxy[gl_VertexID];
	vuv= luv[gl_VertexID];
	vec2 p= W*in_p.xy + xy;

	//if(!!(vmod&0x)){//smol
//
	//}

	float z= abs(in_p.z);//negative z is yeah
	//case PERSP
	//case ORTHO
	//p+= z*vec2(3,1);
	//case PARLX
	;

	vec2 pp= vec2(p-W*tr.xy);
	gl_Position.xy= pp/res;
	gl_Position.z= z/8./tr.w;
	gl_Position.w= .5/tr.w;
	vrune= in_rune;
}
	''',
	'''
uint snake(uvec2 p, uint w){ return p.x+p.y*w; }


layout(location=2) uniform uint tick;

smooth in vec2 vuv;
flat in uvec2 vrune;
flat in uint vmod;
out vec4 col;
void main(){
	const int W= 8;
	ivec2 iuv= ivec2(vuv);

	//scroll
	if(false){
		iuv.y+= int(tick)/4;
	}
	//rotate
	uint dir= 0;//tick/4;
	switch(dir%4){
		case 0: break;
		case 1: iuv.x *=-1; iuv.x -= 1; iuv.xy= iuv.yx; break;
		case 2: iuv.xy*=-1; iuv.xy-= 1;                 break;
		case 3: iuv. y*=-1; iuv. y-= 1; iuv.xy= iuv.yx; break;
	}//-1 due neg int mod
	iuv%= W;

	float lum= 0;
	uint rune;
	uint i;
	if(iuv.y<4){//lower
		rune= vrune.x;
		i= snake(iuv,W);
	}
	else{//upper
		rune= vrune.y;
		i= snake(iuv-uvec2(0,4),W);
	}
	lum= float(((1<<i)&rune)!=0);

	const vec4 COLOR_BASE  = vec4(vec3(.45),1.);
	const vec4 COLOR_CURSOR= vec4(0.,.03,.05,1.);
	const vec4 COLOR_BUS   = vec4(vec3(.3),1.);
	const vec4 COLOR_SYM   = vec4(vec3(.8),1.);
	const vec4 COLOR_OP    = vec4(vec3(.7),1.);
	//const vec4 COLOR_= vec4(.,.,.,1.);

	col= vec4(lum)*COLOR_BASE;
	col.a= 1.;
	if(maxv(iuv)==W-1)
		col+= 2./255;

	switch(vmod){
		case 0:
			break;
		case 1:
			col= 1.-col*1.5;
			break;
		case 2:
			//col.rb*= 0.;
			break;
		//cursor
		case 0x4000000:
			col.gb*=2.;
			col+= COLOR_CURSOR;
			break;
		default:
			break;
	}

	//col.a= 1.-abs(gl_FragCoord.z);
	//col.a*= lum;
	//col.a= gl_FragCoord.z==0.?1.:.125;
}
	''')

vbo_runes= glGenBuffers(1)
vao_runes= glGenVertexArrays(1)
glBindVertexArray(vao_runes)
glBindBuffer(GL_ARRAY_BUFFER, vbo_runes)
glEnableVertexAttribArray(0)
glEnableVertexAttribArray(1)
glEnableVertexAttribArray(2)
s= (4+2+1)*4
glVertexAttribIPointer(0, 4, GL_INT,          s, None)
glVertexAttribIPointer(1, 2, GL_UNSIGNED_INT, s, void_p(4*(4)))
glVertexAttribIPointer(2, 1, GL_UNSIGNED_INT, s, void_p(4*(4+2)))
del s
glVertexAttribDivisor(0,1)
glVertexAttribDivisor(1,1)
glVertexAttribDivisor(2,1)
glBindVertexArray(0)

_tick= 0

def invoke():
	global _tick

	glEnable(GL_FRAMEBUFFER_SRGB)
	glEnable(GL_BLEND)
	glDisable(GL_CULL_FACE)
	glDisable(GL_DEPTH_TEST)

	glBindFramebuffer(GL_FRAMEBUFFER, 0)

	c= 1./255.
	glClearColor(c,c,c,0.)
	del c
	glClear(GL_COLOR_BUFFER_BIT)

	glBlendFunc(GL_SRC_ALPHA,GL_ONE)

	#runes
	if 1:
		glBindBuffer(GL_ARRAY_BUFFER, vbo_runes)
		bodies= space.grid.values()
		cursors= space.cursor.insts
		def rrast(b):
			r= b.rune.bin
			return (
				b.p.x,b.p.y,b.z,0,
				r&0xFFFFFFFF,r>>32,
				b.mod
				)
		bodies= [rrast(b) for b in [*bodies,*[c.b for c in cursors]]]
		rarr= numpy.array(bodies,dtype='int32').flatten()
		glBufferData(GL_ARRAY_BUFFER, rarr, GL_DYNAMIC_DRAW)

		prog_rune.bind()
		tr= space.cursor.prime.b.p
		z= 1<<space.cursor.prime.z
		glUniform4i(0,tr.x,tr.y,0,z)
		glUniform2f(1,w,h)
		glUniform1ui(2,_tick)

		glBindVertexArray(vao_runes)
		glDrawArraysInstanced(GL_TRIANGLE_FAN, 0,4, len(bodies))
		
	_tick+= 1
	pygame.display.flip()

