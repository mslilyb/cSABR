import argparse
import glob
import gzip
import json
import os
import sys

from toolbox import FTX

def best_alignment(ref, text):
	if text == 'None': return None
	if '~' not in text: return FTX.parse(text)
	min_dist = 1e9
	min_ali = None
	for astr in text.split('~'):
		ali = FTX.parse(astr)
		s = ref.distance(ali)
		if s < min_dist:
			min_dist = s
			min_ali = ali
		elif s == min_dist:             # this is new
			min_ali.info += f'~{ali}'   # hope it works
			#print('concat', min_ali, file=sys.stderr)
	return min_ali

parser = argparse.ArgumentParser(description='alignment evaluator')
parser.add_argument('dir', help='bakeoff build directory')
parser.add_argument('--minexon', type=int, default=20,
	help='minimum exon length for table3 [%(default)i]')
parser.add_argument('--experimental', action='store_true',
	help='special processing for the synthetic genome experiment')
parser.add_argument('--debug', action='store_true')
parser.add_argument('--verbose', action='store_true')
arg = parser.parse_args()

# Aggregate alignment data by reference read

fps = []
progs = []
for file in glob.glob(f'{arg.dir}/*.ftx.gz'):
	fps.append(gzip.open(file, 'rt'))
	pname = os.path.basename(file)[:-7]
	progs.append(pname)

data = {}
while True:
	lines = []
	for fp in fps: lines.append(fp.readline().rstrip().split())
	if len(lines[0]) == 0: break
	for prog, (ref, ali) in zip(progs, lines):
		if ref not in data: data[ref] = {}
		data[ref][prog] = ali

# Evaluate best alignments and gather summary stats

sumtable = [{}, {}, {}]
with open(f'{arg.dir}/details.txt', 'w') as details:
	for rstr in data:
		ref = FTX.parse(rstr)
		print(ref, file=details)
		for prog in sorted(data[rstr]):
			ali = best_alignment(ref, data[rstr][prog])
			if   ali is None:      r = 'unaligned'
			elif ref.matches(ali): r = 'match'
			elif ref.similar(ali): r = 'partial'
			else:                  r = 'wrong'
			print(f'\t{prog}\t{r}\t{ali}', file=details)
			if len(ref.exons) <= 3: t = sumtable[len(ref.exons) -1]
			if prog not in t: t[prog] = {}
			if r not in t[prog]: t[prog][r] = 0
			t[prog][r] += 1

# Write summary stats

categories = ('match', 'partial', 'wrong', 'unaligned')
for i, table in enumerate(sumtable):
	with open(f'{arg.dir}/table{i+1}.tsv', 'w') as fp:
		print('program\t', '\t'.join(categories), file=fp)
		for prog in sorted(table):
			print(prog, end='\t', file=fp)
			for cat in categories:
				if cat not in table[prog]: n = 0
				else: n = table[prog][cat]
				print(n, end='\t', file=fp)
			print(file=fp)

# More performance metrics...
