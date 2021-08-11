import re

def tokenize(src):
	lines= src.split('\n')
	nums= list(range(len(lines)))

	#remove comments
	cre= re.compile(r'#.*$')
	lines= [ re.sub(cre,'',l) for l in lines]

	lines_stripped= [l.lstrip('\t') for l in lines]
	indents= [len(a)-len(b) for (a,b) in zip(lines,lines_stripped)]
	#indentation equals number of tabs left-stripped
	
	lines= lines_stripped

	#leading non-tab whitespace does not count as indentation
	lines= [l.lstrip().rstrip() for l in lines]

	#listize
	lines= [l.split(' ') for l in lines]

	assert(len(nums)==len(indents)==len(lines))

	#remove empty lines
	(nums,indents,lines)= zip(*[
		(n,d,l) for (n,d,l) in zip(nums,indents,lines)
		if l!=[''] and l!=[]
		])

	return list(zip(nums,indents,lines))

class types:
	int= 'int'

class symbol:
	def __init__(self,name,type):
		self.name= name
		self.type= type

class morph:
	def __init__(self,name,sigin,sigout):
		self.name= name
		self.sigin= sigin
		self.sigout= sigout
		self.arity= (len(sigin),len(sigout))
	def sig_eq(self, i,o):
		return i==self.sigin and o==self.sigout
	def sig_match(self,syms):
		ai= self.arity[0]
		ao= self.arity[1]
		if len(syms)<ai:
			return False#todo

		for i in range(len(syms)):
			a= syms.slice(i,i+ai)
			if a==self.sigin:
				return range(i,i+ai)



morphs= [
	morph('+',(types.int,types.int),(types.int))
	]

def parse(lines):
	for l in lines:
		if 1:
			litany(l)

def litany(l):
	syms= []
	mphs= []
	print(l)
	for s in l[2]:
		if s=='+':
			mphs+=s
			for m in mphs:#iterate the morph stack to attempt consuming
				sm= morph.sig_match(syms)
				if sm:
					popi#remove the matched morphism from the stack
					ret= consume#eval or transpile
					syms+= *ret
		else:
			syms+=s

w= tokenize('''
+ab
a+b
ab+
+a+bc
a+b+c
ab+c+
++abc
a++bc
ab++c
abc++
''')

for e in w:
	print('num:%3i indent:%2i tokens:%s'%e)


w= parse(w)