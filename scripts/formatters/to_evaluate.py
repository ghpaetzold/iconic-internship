import sys

file = sys.argv[1]
out = sys.argv[2]

f = open(file)
o = open(out, 'w')

c = -1
for line in f:
	c += 1
	data = line.strip()
	o.write('nada\t' + str(c) + '\t' + data + '\t' + str(c) + '\n')
f.close()
o.close()
