import sys

f = open(sys.argv[1].strip())
o = open(sys.argv[2].strip(), 'w')

for line in f:
	if len(line.strip())==0:
		print('Empty line!')
		o.write('.\n')
	else:
		o.write(line)
f.close()
o.close()
