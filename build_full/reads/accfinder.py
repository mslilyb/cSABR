from copy import deepcopy
import matplotlib.pyplot as plt
import os
import sys

def gapfinder(ground, weg, thing):
	g = {
	'size': 0,
	'type': None,
	'match': False
	}
	fivep = ground[0][1] - ground[0][0] + 1
	threep = ground[-1][1] - ground[-1][0] + 1
	if fivep < threep:
		typ = 'five'
		siz = fivep
	elif threep < fivep:
		typ = 'three'
		siz = threep
	else:
		typ = 'equal'
		siz = threep

	g['type'] = typ
	g['size'] = siz
	g['match'] = weg
	return g	

files = sys.argv[1:]

strands = ['+','-']

acc = 0
tot = 0
gap = {
	'size': 0,
	'type': None,
	'match': False
}
internal = {
	'gap': None,
	'mesize': 0
}
cases = {
	'ungap': {
		'offsets': [],
		'succ': 0,
	},
	'gapped': {
		'gaps': [],
		'succ': 0
	},
	'iexon': {
		'iexs': [],
		'succ': 0
	}
}

linetypes = ['-', '--', 'o', '-o'] #max 4
pnames = [pn.split('_')[0] for pn in files]
lines = []
l = []
fig, ax = plt.subplots()
for file, pname in zip(files, pnames):
	with open(file, 'rt') as fp:
		for line in fp:
			tot += 1
			fields = line.rstrip().split()
			if line.count('\t') < 1:
				continue

			gt = fields[0].split(',')

			
			exp = fields[3].split(',')

			if len(gt) == 1:
				case = 'ungap'

			elif len(gt) == 2:
				case = 'gapped'

			elif len(gt) == 3:
				case = 'iexon'

			else:
				continue #Invalid length, something went wrong in ground truth.

			for i in range(len(gt)):
				gt[i] = tuple([int(n) for n in gt[i].split('-')])

			for i in range(len(exp)):
				if exp[i] == 'None':
					continue
				exp[i] = tuple([int(n) for n in exp[i].split('-')])

			wegood = True
			if len(exp) != len(gt):
				wegood = False
			else:
				for g, e in zip(gt, exp):
					if g != e:
						wegood = False
			
			if case == 'ungap':
				offset = 'unaligned'
				if exp[0] != 'None':
					offset = gt[0][0] - exp[0][0]
				cases[case]['offsets'].append(offset)
				

			
			elif case == 'gapped':
				cases[case]['gaps'].append(gapfinder(gt, wegood, gap))
			

			elif case == 'iexon':
				ime = deepcopy(internal)
				ime['gap'] = gapfinder(gt, wegood, gap)

				ime['mesize'] = gt[1][1] - gt[1][0] + 1
				cases[case]['iexs'].append(ime)

			if wegood:
				cases[case]['succ'] += 1
				acc += 1


	print('raw accuracy:', acc/tot)
	print('ungapped accuracy:', cases['ungap']['succ'] / len(cases['ungap']['offsets']))
	print('gapped accuracy:', cases['gapped']['succ'] / len(cases['gapped']['gaps']))
	print('internal exon accuracy:', cases['iexon']['succ'] / len(cases['iexon']['iexs']))

'''
	#Plots
	#gapsize vs match, average min gap size...?
	# hacky. 5' first
	match = []
	mmatch = []

	for ga in cases['gapped']['gaps']:
		if ga['type'] != 'five':
			continue

		if ga['match']:
			match.append(ga['size'])
		else:
			mmatch.append(ga['size'])

	fsizes = []
	fres = []

	for i in range(1, 51):
		fsizes.append(i)

		hits = match.count(i)
		misses = mmatch.count(i)

		if hits + misses == 0:
			fres.append(0)
			continue

		fres.append((hits/(hits + misses)) * 100)

	match = []
	mmatch = []

	for ga in cases['gapped']['gaps']:
		if ga['type'] != 'three':
			continue

		if ga['match']:
			match.append(ga['size'])
		else:
			mmatch.append(ga['size'])

	tsizes = []
	tres = []

	for i in range(1, 51):
		tsizes.append(i)

		hits = match.count(i)
		misses = mmatch.count(i)

		if hits + misses == 0:
			tres.append(0)
			continue
		tres.append((hits/(hits + misses)) * 100)
	lines.append((fsizes, fres, tsizes, tres, pname))


	linetype = linetypes[files.index(file)]
	#l1, = ax.plot(fsizes, fres, 'r-', linestyle=linetype)
	#l2, = ax.plot(tsizes, tres, 'b-', linestyle=linetype)
	l.append((ax.plot(fsizes, fres, f'r{linetype}'),))
	l.append((ax.plot(tsizes, tres, f'b{linetype}'),))


ax.legend(tuple(l), labels=(f'5\'DART', f'3\'DART', f'5\'STAR', f'3\'STAR'), loc='upper left', shadow=True)
ax.axis((1,50,0,100 ))
ax.set_xlabel('overhang length')
ax.set_ylabel('percent correct alignments')

ax.set_title(f'Compare:{files}')
fig.savefig(f'plots/fullcomparison.png')
'''