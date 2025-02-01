import argparse
import gzip
import os
import sys

from toolbox import FTX, sam_to_ftx, readfasta

"""
Standalone file conversion for use to standardize outputs from tests
of singularity containers. Used by exactly pblat so far.
"""

# Functions

def sim4file_to_ftxfile(filename, ftxfile=None):
	chrom = None
	strand = None
	exons = []
	ref = None
	n = 0
	with open(filename) as fp:
		if ftxfile is not None: out = open(ftxfile, 'w')
		else:				out = sys.stdout

		for line in fp:
			if line.startswith('seq1 ='):
				if chrom is not None:
					ftx = FTX(chrom, str(n), strand, exons, f'~{ref}')
					print(ftx, file=out)
				chrom = None
				strand = None
				exons = []
				ref = line[7:].split(' ')[0][:-1]
				n += 1
				continue
			elif line.startswith('seq2 ='):
				f = line.split()
				chrom = f[2][:-1]
				continue
			f = line.split()
			if len(f) != 4: continue 
			beg, end = f[1][1:-1].split('-')
			exons.append((int(beg) -1, int(end) -1))
			st = '+' if f[3] == '->' else '-'
			if strand is None: strand = st
			else: assert(strand == st)
		ftx = FTX(chrom, str(n), strand, exons, f'~{ref}')
		print(ftx, file=out)

# CLI

parser = argparse.ArgumentParser(description=f'file conversion tool for .sim4 to .ftx')
parser.add_argument('infile', type=str, metavar='<file>', help='path to input file in sim4 format')
parser.add_argument('--out', type=str, metavar='<file>', required=False, default=None,
	help='path to desired output file. will create the file if nonexistent, otherwise overwrites. default is stdout')
args = parser.parse_args()

# File Conversion

sim4file_to_ftxfile(args.infile, args.out)

