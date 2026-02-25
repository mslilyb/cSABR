import files
import sys
import tools

fafiles = sys.argv[1:]

for fafile in fafiles:
	ofp = f'{fafile.split('.')[0]}_revcomped.fa'
	
	with open(ofp, 'wt+') as outfile:	
		for defline, seq in files.readfasta(fafile):
			print(f'>{defline}\n{tools.anti(seq)}', file=outfile)