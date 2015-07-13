import sys

f = open(sys.argv[1])
o = open(sys.argv[2], 'w')

for i in range(0, 1000000):
	o.write(f.readline())
f.close()
o.close()
