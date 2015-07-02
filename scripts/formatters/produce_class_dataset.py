import sys

f = open(sys.argv[1].strip())
o = open(sys.argv[2].strip(), 'w')

for line in f:
	ter = float(line.strip())
	score = 6
	if ter>55.0:
		score = 5
	elif ter>40:
		score = 4
	elif ter>25:
		score = 3
	elif ter>10:
		score = 2
	elif ter>0:
		score = 1
	else:
		score = 0
	o.write(str(score) + '\n')

f.close()
o.close()	
