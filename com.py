en= enumerate
ra= range

from dataclasses import dataclass as dcls
PHI= 1.61803398874
PI= 3.14159265359
TAU= 2*PI

resolution= (640*2,480*2)

join2d= lambda a: '\n'.join([''.join(s) for s in a])

flatten2= lambda a: [_ for e in a for _ in e]

