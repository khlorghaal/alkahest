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

pygame.init()
pygame.display.set_mode(com.resolution, DOUBLEBUF | OPENGL)
pygame.display.set_caption('____________________________')
w= com.resolution[0]
h= com.resolution[1]

csh_src= '''

//Aliases
#define vec1 float
#define ivec1 int
#define uvec1 uint
#define len length
#define lerp mix
#define norm normalize
#define sat saturate
#define sats saturate_signed

//Consts
#define PI  3.14159265359
#define TAU (PI*2.)
#define PHI 1.61803399
#define deg2rad 0.01745329251
#define SQRT2 (sqrt(2.))
#define BIG 1e8
#define ETA 1e-4
#define eqf(a,b) ( abs((a)-(b))<ETA )

#define count(_n) for(int i=0; i!=_n; i++)
#define forc(i,_n) for(int i=0; i!=_n; i++)

 vec1 v_i_f(ivec1 v){return  vec1(v);}
 vec2 v_i_f(ivec2 v){return  vec2(v);}
 vec3 v_i_f(ivec3 v){return  vec3(v);}
 vec4 v_i_f(ivec4 v){return  vec4(v);}
ivec1 v_f_i( vec1 v){return ivec1(v);}
ivec2 v_f_i( vec2 v){return ivec2(v);}
ivec3 v_f_i( vec3 v){return ivec3(v);}
ivec4 v_f_i( vec4 v){return ivec4(v);}

float sum ( vec2 v){ return dot(v,vec2(1));}
float sum ( vec3 v){ return dot(v,vec3(1));}
float sum ( vec4 v){ return dot(v,vec4(1));}
  int sum (ivec2 v){ return v.x+v.y;}
  int sum (ivec3 v){ return v.x+v.y+v.z;}
  int sum (ivec4 v){ return v.x+v.y+v.z+v.w;}
float prod( vec2 v){ return v.x*v.y;}
float prod( vec3 v){ return v.x*v.y*v.z;}
float prod( vec4 v){ return v.x*v.y*v.z*v.w;}
  int prod(ivec2 v){ return v.x*v.y;}
  int prod(ivec3 v){ return v.x*v.y*v.z;}
  int prod(ivec4 v){ return v.x*v.y*v.z*v.w;}

float maxv( vec2 a){ return                 max(a.x,a.y)  ;}
float maxv( vec3 a){ return         max(a.z,max(a.x,a.y)) ;}
float maxv( vec4 a){ return max(a.w,max(a.z,max(a.x,a.y)));}
float minv( vec2 a){ return                 min(a.x,a.y)  ;}
float minv( vec3 a){ return         min(a.z,min(a.x,a.y)) ;}
float minv( vec4 a){ return min(a.w,min(a.z,min(a.x,a.y)));}
  int maxv(ivec2 a){ return                 max(a.x,a.y)  ;}
  int maxv(ivec3 a){ return         max(a.z,max(a.x,a.y)) ;}
  int maxv(ivec4 a){ return max(a.w,max(a.z,max(a.x,a.y)));}
  int minv(ivec2 a){ return                 min(a.x,a.y)  ;}
  int minv(ivec3 a){ return         min(a.z,min(a.x,a.y)) ;}
  int minv(ivec4 a){ return min(a.w,min(a.z,min(a.x,a.y)));}

//normalized map to signed
//[ 0,1]->[-1,1]
vec1 nmaps(vec1 x){ return x*2.-1.; }
vec2 nmaps(vec2 x){ return x*2.-1.; }
vec3 nmaps(vec3 x){ return x*2.-1.; }
vec4 nmaps(vec4 x){ return x*2.-1.; }
//normalized map to unsigned
//[-1,1]->[ 0,1]
vec1 nmapu(vec1 x){ return x*.5+.5; }
vec2 nmapu(vec2 x){ return x*.5+.5; }
vec3 nmapu(vec3 x){ return x*.5+.5; }
vec4 nmapu(vec4 x){ return x*.5+.5; }

//[0,1]
float saw(float x){ return mod(x,1.); }
float tri(float x){ return abs( mod(x,2.) -1.); }
  int tri(int x, int a){ return abs( abs(x%(a*2))-a ); }


//normalized map to signed
//[ 0,1]->[-1,1]
#define nmaps(v) ((v)*2.-1.)
//normalized map to unsigned
//[-1,1]->[ 0,1]
#define nmapu(v) ((v)*.5+.5)

#define INT_MAX     0x7FFFFFFF
#define INT_HALFMAX 0x00010000
//using macros preserves generic literal ops
#define fix16_i_f(x) ((x)/INT_HALFMAXF)
#define fix16_f_i(x) ((x)*INT_HALFMAXF)

#define _hash(x) (((x>>16)^x)*0x45d9f3b)
#define hash_i_i(x) _hash(_hash((x)))
#define hash_f_i(x) (      hash_i_i(v_f_i(x))         )
#define hash_f_f(x) (v_i_f(hash_i_i(v_f_i(x)))/INT_MAX)
#define hash_i_f(x) (v_i_f(hash_i_i(     (x)))/INT_MAX)

float vnse_2i_1f(ivec2 p){return nmapu(hash_i_f(hash_i_i(p.x+p.y)+hash_i_i(p.y)));}
vec3  vnse_2i_3f(ivec2 p){return nmapu(
	vec3(
		hash_i_f(hash_i_i(p.x    )+hash_i_i(p.y    )),
		hash_i_f(hash_i_i(p.x+p.y)+hash_i_i(p.y    )),
		hash_i_f(hash_i_i(p.x    )+hash_i_i(p.y-p.x))));}

#define bilerp(st,nn,np,pn,pp) \
	lerp(\
		lerp(nn,pn,st.x),\
		lerp(np,pp,st.x),\
		st.y)






layout(binding=0, rgba16f) writeonly restrict uniform image2D img_o;
#if STAGE_GEOMAG
	;
#else
	layout(binding=0) uniform sampler2D img_i;
	layout(binding=1) uniform sampler2D img_basis;
		//	+textureGrad(img_basis,uv,     vec2(2.5,0.),vec2(0.,2.5))
		//+textureGrad(img_i,    uv,     vec2(1.5.x,0.),vec2(0.,1.5))
	#define sample(uv) (\
		+textureLod(img_basis,uv,0)\
		+textureLod(img_i,    uv,0)\
		)
		//FIXME actually use uv grad lol
#endif
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

	#if (STAGE_FLARE|STAGE_TONEMAP)
		const vec4 bb= 
			#if STAGE_FLARE
				texelFetch(img_basis,ivec2(gid),0)
			#elif STAGE_TONEMAP
				texelFetch(img_i,ivec2(gid),0)
			#endif
			;
	#endif


	#ifdef STAGE_GEOMAG
	{
		float k= 30.;
		ivec2 m= iuv%30;
		float l= float(minv(m)==0);
		col= vec4(l);
	}
	#elif STAGE_FLARE
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
		const int I= 3;
		const int K= 1;
		const vec2 KMUL= res_rcp/K;
		const vec2 rad= 1./res;
		vec4 flare= vec4(0.);

		count(I){
			vec2 r= rad*i;
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
			//const float l= float(i);
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
		//col= bb*EXPOSURE;
		col.rgb/= max(1.,maxv(col.rgb));
		col.a= bb.a;
	}
	#else
		#error no stage #defined
	#endif

	imageStore(img_o, iuv, col);
}
'''
def prog(m):
	try:
		csh_src_p= ''.join([
			'#version 450\n',
			*['#define %s 1\n'%d for d in m],
			'#line 1\n',
			csh_src
		])
		csh_sh= shaders.compileShader(csh_src_p, GL_COMPUTE_SHADER)
		return (shaders.compileProgram(csh_sh),m)
	except Exception as e:
		print('\nSHADERROR\n')
		e= str(e)
		e= e.replace('\\\\n','\n')
		e= e.replace(  '\\n','\n')
		e= e.replace(  '\\t','\t')
		e= e.replace(  '\\t','\t')
		e= e.replace(  '\\','')
		e= e.replace('\\\\','')#fuck
		import re
		e= re.sub(r'\(([0-9]+)\)', r'\nFile "imgls.comp.glsl", line \1', e)
		#sublime default error regex
		print(e)
		exit()

BIGPP= 0
if BIGPP:
	progs= list(map(prog,[
		['STAGE_GEOMAG'],
		*([['STAGE_FLARE']]*8),
		['STAGE_TONEMAP']
		]))
else:
	progs= list(map(prog,[
		['STAGE_GEOMAG'],
		['STAGE_TONEMAP']
		]))

textures= glGenTextures(3)
_pingpong= textures[:2]
tex_basis= textures[ 2]
for i,pp in enumerate(textures):
	glBindTexture(GL_TEXTURE_2D,pp)
	MIPS= 2
	glTexStorage2D(GL_TEXTURE_2D, MIPS, GL_RGBA32F, w,h)#memory uninitialized, inits mipmap level range
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAX_ANISOTROPY_EXT, 4)

wg= (w//8,h//8,1)
def invoke():
	global _pingpong
	for p in progs:
		(p,args)= p
		glUseProgram(p)
		glUniform2f(0,w,h)
		glUniform2i(1,w,h)

		if 'STAGE_GEOMAG' in args:
			glBindImageTexture(0,tex_basis, 0,False,0, GL_WRITE_ONLY, GL_RGBA32F)
		else:
			_pingpong= _pingpong[::-1]

			glActiveTexture(GL_TEXTURE0+0)
			glBindTexture(GL_TEXTURE_2D,_pingpong[0])
			glGenerateMipmap(GL_TEXTURE_2D)

			glActiveTexture(GL_TEXTURE0+1)
			glBindTexture(GL_TEXTURE_2D,tex_basis)

			glBindImageTexture(0,_pingpong[1], 0,False,0, GL_WRITE_ONLY, GL_RGBA32F)

		glDispatchCompute(*wg)
		glMemoryBarrier( GL_SHADER_IMAGE_ACCESS_BARRIER_BIT )

	fb= glGenFramebuffers(1)
	glBindFramebuffer(GL_READ_FRAMEBUFFER, fb)
	glBindFramebuffer(GL_DRAW_FRAMEBUFFER, 0)
	glFramebufferTexture2D(GL_READ_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D,_pingpong[1] if BIGPP else tex_basis, 0)
	glBlitFramebuffer(0,0,w,h,0,0,w,h,GL_COLOR_BUFFER_BIT, GL_NEAREST)
	pygame.display.flip()

#del rast
#rast= glReadPixels(0,0,w,h, GL_RGBA,GL_FLOAT)


#print(rast.shape)
#rast= rast*(-1+2**16)
#rast= rast.astype(np.uint16).flatten()
#print(rast.shape)
#w= png.Writer(
#	size=(w,h),
#	bitdepth=8,
#	greyscale=False,
#	alpha= True,
#	compression=8
#	)

#w.write_array( open('./out.png','wb'), rast )
