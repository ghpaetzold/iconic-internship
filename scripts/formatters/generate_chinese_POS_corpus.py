

f1 = open('/export/data/ghpaetzold/iconicinternship/source.txt')
f2 = open('corpus.txt')
o = open('testando.txt', 'w')

curr = ''
currp = ''
line1 = f1.readline().strip()
for line2 in f2:
	data = line2.strip().split('\t')
	word = data[0]
	tag = data[1]
	curr += word
	currp += tag + ' '
	if len(curr)>=len(line1):
		o.write(currp.strip() + '\n')
		currp = ''
		curr = ''
		line1 = f1.readline().strip()
f1.close()
f2.close()
o.close()
