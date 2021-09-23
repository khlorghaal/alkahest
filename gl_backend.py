import com
import numpy as np
import png
#import exr

import pygame
from pygame.locals import *

import ctypes as ct
from OpenGL.GL import *
from OpenGL.GL import shaders
from OpenGL.GL.EXT.texture_filter_anisotropic import *

import numpy



pygame.init()
pygame.display.set_mode(com.resolution, DOUBLEBUF | OPENGL )
pygame.display.set_caption('____________________________')

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
setwh(*com.resolution)

z=4#2**z
def zoomin():
	global z
	if 1<<z < whmax//8:#max size percentage of screen
		z+=1
def zoomou():
	global z
	if z>0:
		z-=1

tr= np.array((0,0))#view translation

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

	const vec4 bb= 
		#if STAGE_FLARE
			texelFetch(img_basis,ivec2(gid),0)
		#elif STAGE_TONEMAP
			texelFetch(img_basis,ivec2(gid),0)
			+texelFetch(img_i,ivec2(gid),0)
		#endif
		;

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
		const int I= 4;
		const int K= 1;
		const vec2 KMUL= res_rcp/K;
		const vec2 rad= 1./res;
		vec4 flare= vec4(0.);

		count(I){
			vec2 r= rad*_i;
			vec4 acc= vec4(0.);
			for(int x=-K; x<=K; x++){
				for(int y=-K; y<=K; y++){
					const vec2 o= vec2(x,y)*KMUL;
					acc+= 
						+sample(uv + n*r + o )
						+sample(uv - n*r + o )
						+sample(uv + t*r + o )
						+sample(uv - t*r + o );
				}
			}
			//const float l= float(_i);
			const float mag= 1.;///(1.+l*.1);
			flare+= acc*mag;
		}
		const int KDIA= (1+K*2);
		flare/= I*KDIA*4;//normalize

		flare*= .2;//exponential decay or explosion
		col= bb+flare;
	}
	#elif STAGE___
	{
		col= vec4(0.,uv,1.);
	}
	#elif STAGE_TONEMAP
	{
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

PP= 1
PPBIG= 1
if PP:
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



prog_quad= prog_vf('''
layout(location=0) uniform ivec4 tr;
layout(location=1) uniform vec2 res;
layout(location=0) in ivec2 in_qp;
layout(location=1) in ivec3 in_xyt;
smooth out vec2 uv;//ints cant smooth
void main(){
	vec2 p= in_qp + in_xyt.xy - tr.xy;
	gl_Position.xy= (p)/res;
	gl_Position.zw= vec2(0,.5/tr.w);
	uv= in_qp.xy;
}
	''',
	'''
//layout(location= )uniform sampler2D atl;
smooth in vec2 uv;
out vec4 col;
void main(){
	col= vec4(0,uv,1);
}
	''')






quads=[]#(x,y,w,h)
vbo_quad=  glGenBuffers(1)
vbo_quads= glGenBuffers(1)
qv= [
	 0, 0,
	 0, 1,
	 1, 1,
	 1, 0
]
glBindBuffer(GL_ARRAY_BUFFER, vbo_quad)
glBufferData(GL_ARRAY_BUFFER, numpy.array(qv,dtype='int8'), GL_STATIC_DRAW)
#quads filled per frame

vao_quads= glGenVertexArrays(1)
glBindVertexArray(vao_quads)
glEnableVertexAttribArray(0)
glEnableVertexAttribArray(1)
glBindBuffer(GL_ARRAY_BUFFER, vbo_quad)
glVertexAttribIPointer(0, 2, GL_BYTE, 2*1, None)
glBindBuffer(GL_ARRAY_BUFFER, vbo_quads)
glVertexAttribIPointer(1, 3, GL_INT, 3*4, None)
glVertexAttribDivisor(1,1)
glBindVertexArray(0)

def quad(q):
	global quads
	assert(len(q)==3)
	quads+= [q]




#@ds downscale, int
def invoke(sc=1):
	glEnable(GL_FRAMEBUFFER_SRGB)
	glEnable(GL_BLEND)
	glDisable(GL_CULL_FACE)
	glDisable(GL_DEPTH_TEST)

	if PP:
		glBindFramebuffer(GL_FRAMEBUFFER, fb)
	else:
		glBindFramebuffer(GL_FRAMEBUFFER, 0)

	#draw quads
	glBindBuffer(GL_ARRAY_BUFFER, vbo_quads)
	qarr= numpy.array(quads,dtype='int32').flatten()
	glBufferData(GL_ARRAY_BUFFER, qarr, GL_DYNAMIC_DRAW)



	prog_quad.bind()
	global tr
	glUniform4i(0,tr[0],tr[1],0,1<<z)
	glUniform2f(1,w,h)

	glBindVertexArray(vao_quads)
	glDrawArraysInstanced(GL_TRIANGLE_FAN, 0,4, len(quads))
	quads.clear()



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
	glClearColor(0,0,0,0)
	glClear(GL_COLOR_BUFFER_BIT)