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
from OpenGL.GL.EXT.texture_filter_anisotropic import *

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

z=2#2**z
def zoomin():
	global z
	if 1<<z < whmax//64:#max size percentage of screen
		z+=1
def zoomou():
	global z
	if z>0:
		z-=1





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




csh_src= '''

layout(binding=0, rgba16f) writeonly restrict uniform image2D img_o;

layout(binding=0) uniform sampler2D img_i;
layout(binding=1) uniform sampler2D img_basis;
	//	+textureGrad(img_basis,uv,     vec2(2.5,0.),vec2(0.,2.5))
	//+textureGrad(img_i,    uv,     vec2(1.5.x,0.),vec2(0.,1.5))
#define sample(uv) (\
	+textureLod(img_basis,uv,0)\
	+textureLod(img_i,    uv,0)\
	)
//"Store operations to any texel that is outside the boundaries of the bound image will do nothing."

layout(location=0) uniform  vec2  res;
layout(location=1) uniform ivec2 ires;
const vec2 res_rcp= 1./res;	

layout(
	local_size_x= 8,
	local_size_y= 8,
	local_size_z= 1
	) in;

#ifndef STAGE0
	//shared vec4 sh[8][8];
#endif

void main(){
	ivec2 iuv= ivec2(gl_GlobalInvocationID.xy);
	 vec2  uv=  vec2(iuv+.5)/res;
	 vec2 uvn= uv;
	 uvn= nmaps(uvn);
	 uvn.x*=(res.x/res.y);

	vec4 col;

	uvec2 gid= gl_GlobalInvocationID.xy;
	uvec2 lid=  gl_LocalInvocationID.xy;
	uvec2 lsz= gl_WorkGroupSize.xy;

	const int I= 6;
	const int K= 2;

	vec4 bb= texelFetch(img_basis,ivec2(gid),0);

	#if STAGE_FLARE
	{
		const vec2 focus= vec2(0.,.0);
		vec2 uv= uv;
		vec2 d= uvn-focus;
		vec2 n= norm(d);
		const float ld= len(d);
		//n/= 1.-pow(ld,.2);
		//n*= 1.-1./(1.+ld*4.);
		vec2 t= n.yx; t.y=-t.y;
		col= bb;
		const vec2 KMUL= res_rcp/K;
		const vec2 rad= 1./res;
		vec4 flare= vec4(0.);

		count(I){
			vec2 r= rad*_i;
			for(int x=-K; x<=K; x++){
				for(int y=-K; y<=K; y++){
					const vec2 o= vec2(x,y)*KMUL;
					vec4 acc= 
						+sample(uv + n*r + o )
						+sample(uv - n*r + o )
						+sample(uv + t*r + o )
						+sample(uv - t*r + o );
					float atten= len(o);
					flare+= acc*atten;
				}
			}
		}
		col= flare;
	}
	#elif STAGE___
	{
		col= vec4(0.,uv,1.);
	}
	#elif STAGE_TONEMAP
	{
		const int KDIA= (1+K*2);
		float ppmag= I*KDIA*4;//normalize
		ppmag*= .0000004;

		vec4 ppbb= texelFetch(img_i,ivec2(gid),0);
		bb+= ppbb*ppmag;
		const float EXPOSURE= 1.;
		//col= 1.-1./(bb*EXPOSURE+1.);
		col= 1.-exp(-bb*EXPOSURE);
		col.rgb/= max(1.,maxv(col.rgb));
		col.a= bb.a;
	}
	#else
		#error no stage or invalid stage #defined
	#endif

	imageStore(img_o, iuv, col);
}
'''
PP= 0
PPBIG= 1
if PP:
	brek#fixme pp broke
	if PPBIG:
		STAGES= [
			*([['STAGE_FLARE']]*2),
			['STAGE_TONEMAP']
			]
	else:
		STAGES= [['STAGE_TONEMAP']]
	pp_progs= list(map(lambda f: prog_c(csh_src,f),STAGES))

	textures= glGenTextures(3)
	_pingpong= textures[:2]
	tex_basis= textures[ 2]
	for t in textures:
		glBindTexture(GL_TEXTURE_2D,t)
		MIPS= 1
		glTexStorage2D(GL_TEXTURE_2D, MIPS, GL_RGBA32F, w,h)#memory uninitialized, inits mipmap level range
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
		#glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAX_ANISOTROPY_EXT, 4)
	fb= glGenFramebuffers(1)
	glBindFramebuffer(GL_FRAMEBUFFER, fb)
	glFramebufferTexture2D(GL_READ_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D,tex_basis, 0)
	wg= (w//8,h//8,1)



prog_rune= prog_vf('''
layout(location=0) uniform ivec4 tr;
layout(location=1) uniform vec2 res;
layout(location=0) in ivec4 in_p;
layout(location=1) in uvec2 in_rune;
layout(location=2) in uint  in_mod;
smooth out vec2 vuv;//ints cant smooth
flat out uvec2 vrune;
flat out uint  vmod;
void main(){
	const int W= 8;
	const int W2= W/2;
	const ivec2[] lxy= ivec2[](
		ivec2(-W2,-W2),
		ivec2(-W2, W2),
		ivec2( W2, W2),
		ivec2( W2,-W2)
	);
	ivec2 xy= lxy[gl_VertexID];
	vec2 p= W*in_p.xy + xy;

	float z= in_p.z;
	//case PERSP
	//case ORTHO
	p+= z*vec2(3,1);
	//case PARLX
	;

	gl_Position.xy= vec2(p-W*tr.xy)/res;
	gl_Position.z= z/8./tr.w;
	gl_Position.w= .5/tr.w;
	const vec2[] luv= vec2[](
		ivec2( 0, 0),
		ivec2( 0, W),
		ivec2( W, W),
		ivec2( W, 0)
	);
	vuv= luv[gl_VertexID];
	vrune= in_rune;
	vmod= in_mod;
}
	''',
	'''
uint snake(uvec2 p, uint w){ return p.x+p.y*w; }

smooth in vec2 vuv;
flat in uvec2 vrune;
flat in uint vmod;
out vec4 col;
void main(){
	const int W= 8;
	ivec2 iuv= ivec2(vuv);

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

	col= vec4(lum);
	//col= vec4(0.,vuv/float(W),1.);
	col.rgb*= .65;
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
		default:
			break;
	}

	//col.a= 1.-abs(gl_FragCoord.z);
	col.a= 1.;
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



def invoke():
	glEnable(GL_FRAMEBUFFER_SRGB)
	glEnable(GL_BLEND)
	glDisable(GL_CULL_FACE)
	glDisable(GL_DEPTH_TEST)

	if PP:
		glBindFramebuffer(GL_FRAMEBUFFER, fb)
	else:
		glBindFramebuffer(GL_FRAMEBUFFER, 0)

	c= 1./255.
	glClearColor(c,c,c,0.)
	del c
	glClear(GL_COLOR_BUFFER_BIT)

	glBlendFunc(GL_SRC_ALPHA,GL_DST_COLOR)

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
		glUniform4i(0,tr.x,tr.y,0,1<<z)
		glUniform2f(1,w,h)

		glBindVertexArray(vao_runes)
		glDrawArraysInstanced(GL_TRIANGLE_FAN, 0,4, len(bodies))
		
	if PP:
		global _pingpong
		for p in pp_progs:
			p.bind()
			glUniform2f(0,w,h)
			glUniform2i(1,w,h)

			_pingpong= _pingpong[::-1]

			glActiveTexture(GL_TEXTURE0+0)
			glBindTexture(GL_TEXTURE_2D,_pingpong[0])
			glGenerateMipmap(GL_TEXTURE_2D)

			glActiveTexture(GL_TEXTURE0+1)
			glBindTexture(GL_TEXTURE_2D,tex_basis)

			glBindImageTexture(0,_pingpong[1], 0,False,0, GL_WRITE_ONLY, GL_RGBA32F)

			glDispatchCompute(*wg)
			glMemoryBarrier( GL_SHADER_IMAGE_ACCESS_BARRIER_BIT )

		#glBlitFramebuffer(0,0,w,h,0,0,w*sc,h*sc,GL_COLOR_BUFFER_BIT, GL_NEAREST)
		#fb= glGenFramebuffers(1)
		glBindFramebuffer(GL_READ_FRAMEBUFFER, fb)
		glBindFramebuffer(GL_DRAW_FRAMEBUFFER, 0)
		glFramebufferTexture2D(GL_READ_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D,_pingpong[1], 0)
		#fixme dont rebind fbtexture
		glBlitFramebuffer(0,0,w,h,0,0,w,h,GL_COLOR_BUFFER_BIT, GL_NEAREST)
		#glBindFramebuffer(GL_READ_FRAMEBUFFER, fb)
		#glFramebufferTexture2D(GL_READ_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D,tex_basis, 0)

	pygame.display.flip()

