import files
import os
import sys

filedir = sys.argv[1]
strand = sys.argv[2]

strands = ['+', '-']

if strand not in strands:
	strand = None

path = os.path.abspath(filedir)

for entry in os.scandir(path):
	if not entry.is_file():
		continue
	elif not entry.name.endswith('.gz') and not entry.name.endswith('.ftx'):
		continue

	pname = entry.name.split('.')[0]

	with files.getfp(entry.path) as fp, open(f'{pname}_reads.tsv', 'w') as ofp:
		for line in fp:
			results = line.rstrip().split()

			ground, exper = results[0], results[1]

			gfields = ground.split('|')
			efields = exper.split('|')



			ejunc = 'None'
			erstrand = 'None'

			if '|' in exper:
				ejunc = efields[3]
				erstrand = efields[2]

			grjunc = gfields[3]


			gestrand, grstrand = gfields[2], gfields[4][1]


			oline = '\t'.join([grjunc, gestrand, grstrand, ejunc, erstrand])


			if strand != None and gestrand != strand:
				continue

			else:
				print(oline, file=ofp)

