from space import body

'''
funpy
ent int int
	add
ret int
'''

from com import *
import rune

@dcls
class op:
	ai: int# input arity
	ao: int#output arith
	f: str

#explicit binary ops
_add= lambda a,b: a+b

sym_op={
	'add': op(2,1,'_add'),
}

def parse(runes:list[list[str]]):
	src= ''
	stak= []
	for y,l in en(runes):
		for x,sym in en(l):
			val= f'v_{y}_{x}'

			if not sym[0].isalpha():#number literal
				line= f'{val}= {sym}'
				stak+=[val]

			else:
				op= sym_op[sym]
				args= ','.join([stak.pop() for i in ra(op.ai)])
				line= f'{val}= {op.f}({args})'
				if op.ao==1:
					stak+=[f'{val}']
				else:
					for v in ra(op.ao):
						stak+=[f'{val}[{v}]']

			src+= line+'\n'

	ret= ','.join([s for s in stak])
	src+= f'ret=[{ret}]'

	return src+'\n'

def repl(syms:list[list[str]]):
	src= parse(syms)
	print(src)
	print()
	cpl= compile(src,'repl','exec')
	ret={}
	exec(cpl,globals(),ret)
	print(ret['ret'])
	print()

repl([
	['1','1'],
	['add']
])