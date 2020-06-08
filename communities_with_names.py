id_fr = open('results\\id _ names.txt', 'r')
txt = open('results\\communities.txt', 'r')
comm_names = open('results\\communities_with_names.txt', 'w')

fr_id ={}
for line in id_fr:
	arr = line.split()
	fr_id.update({arr[0]: arr[1:]})
for line in txt:
	if line != '\n':
		line = line.strip()
		s = str()
		for n in fr_id.get(line):
			s += n
			s += ' '
		comm_names.write(line+ ' ' + s)
		comm_names.write('\n')
	if line == '\n':
		comm_names.write('\n')


txt.close()
comm_names.close()
id_fr.close()