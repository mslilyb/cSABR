import sys
from toolbox import FTX

book = {}
with open(f'{sys.argv[1]}/details.txt') as fp:
	ref = None
	for line in fp:
		if not line.startswith('\t'):
			ref = line.rstrip()
			if ref not in book: book[ref] = []
		else:
			prog, anno, astr = line.lstrip().rstrip().split()
			if astr == 'None': ftx = None
			else:              ftx = FTX.parse(astr)
			book[ref].append((prog, ftx, anno))

for rstr in book:
	ref = FTX.parse(rstr)
	if len(ref.exons) != 1: continue
	annos = set()
	for prog, ali, anno in book[rstr]: annos.add(anno)
	if len(annos) == 1 and 'match' in annos: continue
	print(ref)
	for prog, ali, anno in book[rstr]:
		print('\t',prog, anno, ali)
