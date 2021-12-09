from com import *

boxpals= [
'''
┌┬─┐
├┼┤│
└┴┘ 
''',
'''
┏┳━┓
┣╋┫┃
┗┻┛ 
''',
'''
╔╦═╗
╠╬╣║
╚╩╝ 
''',
'''
╓╥─╖
╟╫╢║
╙╨╜ 
''',
'''
╒╤═╕
╞╪╡│
╘╧╛ 
''']
norm= 0
bold= 1
double= 2
double_w= 3 
double_h= 4
print(boxpals)
boxpals= [boxpal.replace('\n','') for boxpal in boxpals]
print(boxpals)
keydirs= [
 'ds', 'ads', 'ad','as',
'dsw','adsw','asw','sw',
 'dw', 'adw', 'aw','']
dir_normalise= lambda d: ''.join(sorted(d))
keydirs= [dir_normalise(k) for k in keydirs]

assert(all([len(p) for p in boxpals]))
assert(len(boxpals[0])==len(keydirs))

dict_key_boxpal= {k:v for k,v in zip(keydirs,boxpals[0])}
dict_boxpal_key= {v:k for k,v in zip(keydirs,boxpals[0])}
print(' ; '.join(['%1s:%3s'%(k,v) for k,v in dict_boxpal_key.items()]))

node= lambda edges: ''.join([dict_key_boxpal[dir_normalise(e)] for e in edges])
nds= lambda e: '\n'.join([node(l.split(' ')) for l in e.split('\n')])

if 1:
  print(nds('''
  ds ad ad ad sa ds
  sw    sw sw
  dw ad da da wa dw
  aw sw dw    ds sw as
  ad wasd ad    ad  da
  sa sw ds    dw sw aw
  ds as   aw dw    wasd swda
  dw aw   sa ds    dasw daws
  ds as
  aw aw
  '''))
for i in ra(32): print()

grid= {}
def blit(rast,p=(0,0)):
  (w,h)= (len(rast),len(rast[0]))
  for y,l in enumerate(rast):
    for x,v in enumerate(l):
      grid[(x+p[0],y+p[1])]= v
def flush():
  ps= grid.keys()
  xs=[_[0] for _ in ps]
  ys=[_[1] for _ in ps]
  if len(grid)==0:
    print()
    return
  (w0,h0)= (min(xs),min(ys))#inclusive
  (w1,h1)= (max(xs),max(ys))#exclusive
  w1+= 1
  h1+= 1
  w= w1-w0
  h= h1-h0

  #print(' '.join([str(_) for _ in [w,h,w0,h0,w1,h1]]))
  bg= ' '
  rast= [[bg for _ in range(w0,w1)] for __ in range(h0,h1)]
  for p in ps:
    rast[p[1]-h0][p[0]-w0]= grid[p]

  gl_backend.blit(rast)
  gl_backend.invoke()

  COUT=0
  if COUT:
    print(join2d(rast[::-1]))#y up
  grid.clear()

#import time
#for i in range(w-2):
#  blit(['┓'],( w//2, h//2))
#  blit(['┛'],( w//2,-h//2))
#  blit(['┏'],(-w//2, h//2))
#  blit(['┗'],(-w//2,-h//2))
#
#  curs= nds('''
#ds sw sa
#sw  da
#dw da aw''').split('\n')[::-1]
#
#  blit(curs,(i-w//2,i-h//2))
#  flush();
#  time.sleep(1./20)



#import gl_backend
#import pygame
#while(1):
#    blit(['asdf','qwer','zxcv'])
#    flush()
#    for event in pygame.event.get():
#        if event.type == pygame.QUIT:
#            exit()





'''
├─────┐
├━━┓  ├━━┓
┃<<│8 ┃* │hb
├━━┛  ├━━┛
│     │
├━━┓  │
┃* │ha│
├━━┛  │
│     │
├━━┓  │
┃- │──┘
├━━┛  
║


├───────────┐
├─────┐     │
├───────────┤
├─────┘     │
├───────────┘

arity is the surface connections and their sign

┌───┐
│   │
└───┘
┌┴┴┴┐
┤   ├
└┬┬┬┘
┏───┓
│   │
┗───┛
┏─┴─┓
┤   ├
┗─┬─┛
├━━━┤
┃   ┃
├━━━┤

  │
  │
  │
─────

#djb
uint -> uint
ha= 0x6487d51ul
hb= 0x45d9f3bul
return (x<<8)*ha-x*hb;

a= x<<8
c= x*hb
b= a*ha
d= b-c
ret

x─┬<<──*─ -═
  │ 8 ha  │ 
  *───────┘
  hb

 x
 ├──┐
<<8 *hb
 │  │
 *ha│
 │  │
 - ─┘
 ║


┃  
├─────┐
├━━┓  ├━━┓
┃<<│8 ┃* │hb
├━━┛  ├━━┛
│     │
├━━┓  │
┃* │ha│
├━━┛  │
│     │
├━━┓  │
┃- │──┘
├━━┛  
║

#carpet#
join2d= lambda a: '\n'.join([''.join(s) for s in a])
c= lambda w,h: join2d([[ ' ' if (abs(x*2-w)+abs(y*2-h))%10>=6 else '▉' for x in range(w)] for y in range(h)])
print(c(32,12))
          
                                               
          
          
          ┏━━━┓                               
          ┃ 𝝺 │str | list < str
          ├━━━┤     
          ├━━━┤                               
          ┃.()│join ┏━━━┓                                                             
┏━━━┓     ┗━┬━┛     ┃ F │join2              
┃ " |''     ║       ┗━┬━┛ list < list < str                  
┗━━━┴────┬┬━┻━┓       |  
┏━━━┓    │┃ 𝝠 ┃     ┏━┴━┓ 
┃ " |'\n'│┗━┳━┻━━━━━┫map┃
┗━━━┴────┘  ┃       ┗━┬━┛ list < str
            ┃       ┏━┴━┓         
            ┗━━━━━━━┫( )┃     
                    ┗━┬━┛ str
                      ║

      ┏━━━┓              
      ┃vi2│ 32 | 32
      ┗━┬━┤   
      ┏━┴━┤    │vi2   │vi2
      ┃for━━━━━┳━━━━━━┓
      ┗━┬━┛    ├━━━┓  │    
      ┏━┴━┓    ┃ * │2 │                              
 join2│( )┃    ├━━━┛  │                               
      ┗━┬━┛    ├━━━┓  │                              
        ║      ┃ - ├──┘                           
               ┗━┬━┛                         
               ┏━┴━┓                         
               ┃|+|┃                      
               ┗━┬━┛                    
               ┏━┴━┓                  
               ┃ 𝝨 ┃             
               ├━━━┛               
               ├━━━┓              
               ┃ % │10             
               ├━━━┛              
               ├━━━┓              
               ┃ >=│6             
               ┗━┬━┛               
               ┏━┴━┓              
            ' '│:?.│'▉'             
               ┗━┬━┛              
                 ║                           
              
              
              
              
              
arithmetic composition
asc= lam   f: lam a,b: fold(f,[1]*b*a) 
add= lam a,b: a+b
mul= lam a,b: asc(add)
pow= lam a,b: asc(mul)

foof asc
        
              




fun jn2 list of list of str
[str void]
.join
<-
[str '\n']
.join
^

   ──┘  │

┄┈╌
┅┉╍
--
╏┆┇┊┋╎||||
┏┳━┓
┣╋┫┃
┗┻┛
┌┬─┐
├┼┤│
└┴┘
╔╦═╗
╠╬╣║
╚╩╝
╓╥─╖
╟╫╢║
╙╨╜
╒╤═╕
╞╪╡│
╘╧╛
┎┒┍┑
┖┚┕┙
┝┞┟┠┡┢
┥┦┧┨┩┪
┭┮┯
┰┱┲┵
┶
┷┸┹┺
┽
┾┿
╀
╁
╂
╃
╄
╅
╆
╇
╈
╉
╊



'''