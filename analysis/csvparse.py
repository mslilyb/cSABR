import argparse
from copy import deepcopy
import files
import glob
import os
import random
import sys

"""
Quick and Dirty script to take all the csvs in a folder and do some summaries on them. Takes in a directory as an argument, parses 
all files with the .csv extension. Compressed ok.

arguments: Fields

by-field/case

statistics, desciptive?

for now, just will do all the things i want. the extensible thing may be useful if i have to do it a ton. first function, then ability.
"""
def makeweights(wlist):
	total = sum(wlist)
	print(total)
	for i in range(len(wlist)):
		wlist[i] /= total

	return wlist

directory = sys.argv[1]

path =  os.path.abspath(directory)

print(path)

filecounts = []
cases = {
	'all': {'counts': [], 'weights': [], 'averages': []}, 
	'unspliced': {'counts': [], 'weights': [], 'averages': []}, 
	'spliced': {'counts': [], 'weights': [], 'averages': []}, 
	'internal': {'counts': [], 'weights': [], 'averages': []} 
}

#exnamelist = []

olens = {
	'all': {},
	'equal': {},
	'fivep': {},
	'threep': {}
}

olentmplate = {
	'count': 0,
	'average': 0,
	'weight': 0
}



for file in sorted(glob.glob(f'{directory}/*.csv*')):
	title = True
	cases['all']['counts'].append(0)	
	cases['unspliced']['counts'].append(0)	
	cases['spliced']['counts'].append(0)	
	cases['internal']['counts'].append(0)

	covsum = {
		'all': 0,
		'unspliced': 0,
		'spliced': 0,
		'internal': 0
	}

	olcovs = {
		'otyp': [],
		'len': [],
		'cov': []
	}



	with files.getfp(file) as fp:
		for line in fp:
			fields = line.rstrip().split(',')
			
			if title:
				title = False
				cov_index = fields.index('coverage')
				print(fields)
				case_index = fields.index('case')
				oh_type_index = fields.index('oh_type')
				oh_len_index = fields.index('oh_len')
				continue

			coverage = float(fields[cov_index])
			case = fields[case_index]
			oh_type = fields[oh_type_index]
			oh_len = fields[oh_len_index]
			#exnamelist.append(fields[fields.index('ex_read')])

			cases['all']['counts'][-1] += 1

			cases[case]['counts'][-1] += 1

			covsum['all'] += coverage
			covsum[case] += coverage

			olcovs['otyp'].append(oh_type)
			olcovs['len'].append(oh_len)
			olcovs['cov'].append(coverage)

	# make averages
	
	for case in cases.keys():
		cases[case]['averages'].append(covsum[case] / cases[case]['counts'][-1])

		cases[case]['weights'].append(cases[case]['counts'][-1])


	#handle o_lens

	for ot, l, c, in zip(olcovs['otyp'], olcovs['len'], olcovs['cov']):
		if l not in olens['all']:
			olens['all'][l] = deepcopy(olentmplate)

		if l not in olens[ot]:
			olens[ot][l] = deepcopy(olentmplate)


		olens['all'][l]['count'] += 1
		olens['all'][l]['average'] += c

		olens[ot][l]['count'] += 1
		olens[ot][l]['average'] += c



	# calc their averages

	for case in olens.keys():
		for le in olens[case].keys():

			for i in range(len(olens[case][le]['count'])):
				olens[case][le]['average'][i] /= olens[case][le]['count'][i]


	


