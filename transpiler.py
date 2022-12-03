#im ditching this for now in favor of a python vm
#its just the best thing for prototyping




#text itself is dead stone
#a compiler brings life to symbols
#the living symbols are the catalyst of omega
#	what the fuck does this mean
#	i definitely wrote this while high


'''
funpy
ent int int
	add
ret int
'''

from com import *

@dcls
class op:
	ai: int# input arity
	ao: int#output arity
	f: str

#binary infix
_add= lambda a,b: a+b
_mul= lambda a,b: a*b
#acommutative
_sub= lambda a,b: a-b
_div= lambda a,b: a/b
_pow= lambda a,b: a**b
_log= lambda a,b: log(a,b)

def gtok(s):
	s= s[1:-2].split('\n')
	return [ a.strip().split(' ') for a in s ]

sym_op={ a: op(int(b),int(c),d) for a,b,c,d in gtok('''
add 2 1 _add
sub 2 1 _sub
mul 2 1 _mul
div 2 1 _div
pow 2 1 _pow
log 2 1 _log
fft 1 1 fft
rfft 1 1 rfft
ifft 1 1 irfft
irfft 1 1 rfft
''')}

isnop= lambda s: s=='nop'
isliteral= lambda s: not ( s[0].isalpha() or (s[0] in '_') )
isop= lambda s: s in sym_op.keys()
isvar= lambda s: todo

mangle= lambda x,y: f'v_{y}_{x}'

def parse(runes:list[list[str]]):
	src= ''
	varstak= []#:str
	opstak=  []#:str
	#todo FOOF

	def line(l):
		nonlocal src
		src+= l+'\n'

	for y,l in en(runes):
		for x,tok in en(l):
			#generate the line and add it to the stack
			sym= mangle(x,y)#symbol named as grid location

			def consume(op):
				nonlocal varstak
				nonlocal opstak
				nonlocal sym
				args= ','.join([varstak.pop() for i in ra(op.ai)])#stack consumption per op input arity

				#eval and store into symbol
				line(f'{sym}_o= {op.f}({args})')
				#generate output symbols
				out= lambda i: f'{sym}_o_{i}'
				if op.ao==1:
					line(f'{sym}_o_0= #assume whatever the fuck this is can be ignored{sym}_o')
				else:
					for i in ra(op.ao):
						line( out(i)+f'= sym[{i}]')
				#stack output symbols
				for i in ra(op.ao):#return value is list
					varstak+=[out(i)]#filo

			if isnop(tok):
				line(f'{sym}= []')
			elif isliteral(tok):
				line(f'{sym}= {tok}')
				varstak+=[sym]
			elif isop(tok):
				op= sym_op[tok]
				line(f'{sym}= {op.f}')#todo sig
				#todo FOOF
				opstak+= [tok]

			if len(opstak)>0:#an op is waiting to consume
				op= sym_op[opstak[-1]]#only most recent op may consume
				if len(varstak)>=op.ai:
					consume(op)
					opstak.pop()

	if len(varstak)<=0:
		print('WARN: no varstack returned')
		varstak+= [[]]
	if len(opstak)>0:
		print('WARN: opstak remainder: %s'%opstak)

	src+= 'ret    = [ %s ]\n'%(' , '.join(varstak))#output value
	src+= 'ret_sym= [%s]\n'%(','.join([f'\'{s}\'' for s in varstak]))#output symbol
	return src

def rpep(syms:list[list[str]]):
	print('read')
	print(syms)

	print('parse')
	p= parse(syms)
	print(p)

	cpl= compile(p,'rep','exec')#builtin::compile
	out={}
	exec(cpl,globals(),out)

	print('eval')
	print('ret= %s\n'%out['ret'])
	#all symbols may be accessed from `out`
	# ret is the output variable reserved/fixed name in read eval print
	return out

def repl():
	pass

def tests():
	rpep(gtok('''
1 add 2 3 4 add
5 mul 6
div 2 69
	'''))
