from sys import argv
#import random
path1 = argv[1]
path2 = argv[2]

test = open(path1, 'r')
n1 = None
for line in test:
    if line.find('== SCF ENDED - CONVERGENCE ON ENERGY') != -1:
        n1 = float(line.split()[8])
        break

test = open(path2, 'r')
n2 = None
for line in test:
    if line.find('== SCF ENDED - CONVERGENCE ON ENERGY') != -1:
        n2 = float(line.split()[8])
        break
if n1 is None or n2 is None:
    print(0)

n = abs((n1 - n2) / n1)
if n > 0.00001:
    print(0)
else:
    print(1)
#d = random.randint(0, 1)
#print(d)