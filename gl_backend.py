from com import *

import rune
import space
import atom

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
	glViewport(0,0,w,h)#todo
setwh(*resolution)

zoomin= lambda:	zoom(z+1)
zoomou= lambda:	zoom(z-1)


pygame.init()
display= pygame.display
display.gl_set_attribute(pygame.GL_ACCELERATED_VISUAL, 1)
display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 4)
display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 5)
display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
display.gl_set_attribute(pygame.GL_FRAMEBUFFER_SRGB_CAPABLE, 1)
display.set_mode(resolution, DOUBLEBUF | OPENGL )
display.set_caption('____________________________')

import re
@dcls
class prog:
	pid= -1
	unis= {}
	ulocs= {}

	def bind(self):
		glUseProgram(self.pid)
	def shex(e):
		print('\nSHADERROR\n')
		e= str(e)
		e= e[:e.find('[b\"#version')]
		e= e.replace('\\\\n','\n')
		e= e.replace(  '\\n','\n')
		e= e.replace(  '\\t','\t')
		e= e.replace(  '\\t','\t')
		e= e.replace(  '\\','')
		e= e.replace('\\\\','')#fuck
		print(e)
		exit()
	def shpp(src,flags=[]):
		return '\n'.join([
			'#version 450',
			*['#define %s 1'%d for d in flags],
			open('shaderheaders/base.glsl').read(),
			_LOCALHEADER,
			f'#line {lineno(2)}',
			src
		])
def prog_vf(vert,frag,flags=[]):
	self= prog()
	try:
		vert= prog.shpp(vert,flags)
		frag= prog.shpp(frag,flags)
		ivert= shaders.compileShader(vert, GL_VERTEX_SHADER)
		ifrag= shaders.compileShader(frag, GL_FRAGMENT_SHADER)
		self.pid= shaders.compileProgram(ivert,ifrag)
	except Exception as e:
		prog.shex(e)
	return self
def prog_c(prog):
	self= prog()
	try:
		src_p= prog.shpp(src,flags)
		sh= shaders.compileShader(src_p, GL_COMPUTE_SHADER)
		self.pid= shaders.compileProgram(sh)
	except Exception as e:
		prog.shex(e)
	return self


_LOCALHEADER= f'#line {lineno()}'+'''
layout(location=0) uniform ivec4 tr;
layout(location=1) uniform vec2 res;
layout(location=2) uniform long tick;

vec4 project(ivec2 xy, int z, ivec2 align){
	if(z==0)
		z=1;
	z= abs(z);//negative z fuckoff always

	const ivec2 iresh= ivec2(res)/2;
	if(align==ivec2(0)){//world
		xy-= tr.xy;
		xy*= tr.z;
	}
	else{
		xy+= iresh*align;
	}
	xy*= z;
	z=1;
	//todo PERSP PARLX

	return vec4(
		vec2(xy)/res*2.,
		z/256.,
		1.);
}

//const vec4 COLOR_= vec4(.,.,.,1.);
const vec4 COLOR_BASE  =   vec4(vec3(.45),1.);
const vec4 COLOR_BLAND=    COLOR_BASE*.6;
const vec4 COLOR_AKTIV=    v4pad(SKY);
const vec4 COLOR_UNAKTIV=  v4pad(1.-SKY);
const vec4 COLOR_SPICEY=   vec4(1. ,  .3,  .3, 1.);
const vec4 COLOR_HIGHLIGHT=v4pad(TEAL);
const vec4 COLOR_ACHTUNG=  vec4( .5, 1. ,  .1, 1.);
const vec4 COLOR_WARNING=  vec4( YELLOW+.1, 1.);
const vec4 COLOR_DANGER=   v4pad(RED*2.);
const vec4 COLOR_PRIMARY=  vec4(COLOR_BASE.rgb*1.2, 1.);
const vec4 COLOR_CURSOR=   vec4(0. , .03, .05, 1.);

const vec4 COLOR_BUS   =   vec4(vec3(.3),1.);
const vec4 COLOR_SYM   =   vec4(vec3(.8),1.);
const vec4 COLOR_OP    =   vec4(vec3(.7),1.);
const vec4 COLOR_VERBOTEN= vec4( .5,  .1,  .2, 1.);

uint snake(uvec2 p, uint w){ return p.x+p.y*w; }

'''
from space import mods
mods= mods.items()
# const uint MOD_##= ...
_LOCALHEADER+=''.join([f'const uint MOD_{sym.upper()}= {val};\n' for sym,val in mods])



vbo_runes= glGenBuffers(1)
vao_runes= glGenVertexArrays(1)
glBindVertexArray(vao_runes)
glBindBuffer(GL_ARRAY_BUFFER, vbo_runes)
glEnableVertexAttribArray(0)
glEnableVertexAttribArray(1)
glEnableVertexAttribArray(2)
glEnableVertexAttribArray(3)
s= (3+2+1+2)*4
glVertexAttribIPointer(0, 3, GL_INT,          s, void_p(0))
glVertexAttribIPointer(1, 2, GL_UNSIGNED_INT, s, void_p(4*(3)))
glVertexAttribIPointer(2, 1, GL_UNSIGNED_INT, s, void_p(4*(3+2)))
glVertexAttribIPointer(3, 2, GL_INT,          s, void_p(4*(3+2+1)))
del s
glVertexAttribDivisor(0,1)
glVertexAttribDivisor(1,1)
glVertexAttribDivisor(2,1)
glVertexAttribDivisor(3,1)

prog_rune= prog_vf(f'#line {lineno()}'+'''
layout(location=0) in ivec3 in_p;
layout(location=1) in uvec2 in_rune;
layout(location=2) in uint  in_mod;
layout(location=3) in ivec2 in_align;
smooth out vec2 v_uv;//ints cant smooth
flat out uvec2 v_rune;
flat out uint  v_mod;
flat out vec4 v_col;
void main(){
	const ivec2[] lxy= ivec2[](
		ivec2(-4,-4),
		ivec2(-4, 4),
		ivec2( 4, 4),
		ivec2( 4,-4)
	);
	gl_Position= project(
		in_p.xy*8 + lxy[gl_VertexID],
		in_p.z, in_align);

	const vec2[] luv= vec2[](
		ivec2( 0, 0),
		ivec2( 0, 8),
		ivec2( 8, 8),
		ivec2( 8, 0)
	);
	v_uv= luv[gl_VertexID];

	v_rune= in_rune;
	v_mod= in_mod;

	#define L(C,N) case N: v_col= C; break;
	switch(in_mod){
		L(COLOR_BASE,     0)
		L(COLOR_BLAND,    1<< 0)
		L(COLOR_AKTIV,    1<< 1)
		L(COLOR_UNAKTIV,  1<< 2)
		L(COLOR_VERBOTEN, 1<< 3)
		L(COLOR_SPICEY,   1<< 4)
		L(COLOR_HIGHLIGHT,1<< 5)
		L(COLOR_ACHTUNG,  1<< 6)
		L(COLOR_WARNING,  1<< 7)
		L(COLOR_DANGER,   1<< 8)
		L(COLOR_PRIMARY,  1<< 9)
		L(COLOR_CURSOR,   1<<10)
	}
}
''',f'#line {lineno()}'+'''
smooth in vec2 v_uv;
flat in uvec2 v_rune;
flat in uint v_mod;
flat in vec4 v_col;
out vec4 col;
void main(){
	const int W= 8;
	ivec2 iuv= ivec2(v_uv);

	//scroll
	//if(false){
	//	iuv.y+= int(tick)/4;
	//}
	////rotate
	//uint dir= 0;//tick/4;
	//switch(dir%4){
	//	case 0: break;
	//	case 1: iuv.x *=-1; iuv.x -= 1; iuv.xy= iuv.yx; break;
	//	case 2: iuv.xy*=-1; iuv.xy-= 1;                 break;
	//	case 3: iuv. y*=-1; iuv. y-= 1; iuv.xy= iuv.yx; break;
	//}//-1 due neg int mod
	//iuv%= W;

	float lum= 0;
	uint rune;
	uint i;
	if(iuv.y<4){//lower
		rune= v_rune.x;
		i= snake(iuv,W);
	}
	else{//upper
		rune= v_rune.y;
		i= snake(iuv-uvec2(0,4),W);
	}
	lum= float(((1<<i)&rune)!=0);

	col= vec4(lum)*COLOR_BASE;
	col.a= 1.;
	if(maxv(iuv)==W-1)
		col+= 2./255;

	col*= v_col;

	//col.a= 1.-abs(gl_FragCoord.z);
	//col.a*= lum;
	//col.a= gl_FragCoord.z==0.?1.:.125;
}
''')
glBindVertexArray(0)

#todo refactor vaos into a universal

vbo_border= glGenBuffers(1)
vao_border= glGenVertexArrays(1)
glBindVertexArray(vao_border)
glBindBuffer(GL_ARRAY_BUFFER, vbo_border)
glEnableVertexAttribArray(0)#xy
glEnableVertexAttribArray(1)#wh
glEnableVertexAttribArray(2)#proj
glEnableVertexAttribArray(3)#mod
glEnableVertexAttribArray(4)#align
s= 4*(2+2+1+1+2)
glVertexAttribIPointer(0, 2, GL_INT,          s, void_p(4*(0)))
glVertexAttribIPointer(1, 2, GL_UNSIGNED_INT, s, void_p(4*(2)))
glVertexAttribIPointer(2, 1, GL_UNSIGNED_INT, s, void_p(4*(2+2)))
glVertexAttribIPointer(3, 1, GL_UNSIGNED_INT, s, void_p(4*(2+2+1)))
glVertexAttribIPointer(4, 2, GL_INT,          s, void_p(4*(2+2+1+1)))
del s
glVertexAttribDivisor(0,1)
glVertexAttribDivisor(1,1)
glVertexAttribDivisor(2,1)
glVertexAttribDivisor(3,1)
glVertexAttribDivisor(4,1)
prog_bound= prog_vf
(f'#line {lineno()}'+'''
layout(location=0) in ivec3 in_xyz;
layout(location=1) in uvec2 in_wh;
layout(location=2) in uint in_proj;
layout(location=3) in uint in_mod;
layout(location=4) in ivec2 in_align;
flat out vec4 vcol;
void main(){
	//todo mod color
	vcol= COLOR_BASE;

	/*
    x    x 0    1       
     x  x   2  3        
                        
     x  x   4  5   
	x    x 6    7  
	*/
	const uint B= 1;
	const ivec2[] lpos= ivec2[](//indices
		ivec2(0,h),                       ivec2(w,h),
		     ivec2(0+B,h-B), ivec2(w-B,h-B),
		     ivec2(0+B,0+B), ivec2(w-B,0+B),
		ivec2(0,0),                       ivec2(w,0)
	);
	const ivec2[] lxy= ivec2[](//tris
		lpos[0],lpos[1],lpos[3],
		lpos[0],lpos[3],lpos[2],
		lpos[3],lpos[1],lpos[7],
		lpos[3],lpos[7],lpos[5],
		lpos[7],lpos[4],lpos[5],
		lpos[7],lpos[6],lpos[4],
		lpos[6],lpos[0],lpos[2],
		lpos[6],lpos[2],lpos[4]
	);

	gl_Position= project(
		in_xyz.xy + lxy[gl_VertexID],
		in_xyz.z, in_align);
}
	''',f'#line {lineno()}'+'''
flat in vec4 vcol;
out vec4 col;
void main(){
	col= vcol;
}
''')
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

	tr= atom.cursor.prime.b.p
	z= 1<<atom.cursor.prime.zoom
	def unf():
		glUniform4i (0, tr.x*8,tr.y*8,z,z)
		glUniform2f (1, w,h)
		glUniform1ui(2, _tick)

	#glyphs
	if 1:
		glBindBuffer(GL_ARRAY_BUFFER, vbo_runes)
		bodies= space.grid.values()
		def rrast(b):
			g= b.glyph.bin
			assT(b.p,ivec2)
			return (
				b.p.x,b.p.y,b.z,
				g&0xFFFFFFFF,g>>32,
				b.mod, b.align.x, b.align.y
				)
		bodies= [rrast(b) for b in bodies]
		rarr= numpy.array(bodies,dtype='int32').flatten()
		glBufferData(GL_ARRAY_BUFFER, rarr, GL_DYNAMIC_DRAW)


		prog_rune.bind()
		unf()

		glBindVertexArray(vao_runes)
		glDrawArraysInstanced(GL_TRIANGLE_FAN, 0,4, len(bodies))
		
	_tick+= 1
	pygame.display.flip()

