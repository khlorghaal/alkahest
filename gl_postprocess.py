from OpenGL.GL.EXT.texture_filter_anisotropic import *

import ctypes as ct
void_p= ct.c_void_p
from OpenGL.GL import *
from OpenGL.GL import shaders

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

def init():
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

def invoke():
		glBindFramebuffer(GL_FRAMEBUFFER, fb)
		
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
