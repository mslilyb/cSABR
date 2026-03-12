import files
import sys


samfile = sys.argv[1]
pname = sys.argv[2]
DIR = sys.argv[3]

with open (f'{DIR}ftx--{pname}', 'wt') as ofp:
	for entry in files.sam_to_ftx(samfile):
		print(entry, file=ofp)


files.reportalignments('../build_full/reads.fa', f'{DIR}ftx--{pname}', '.', pname)