import argparse
import sys
from toolbox import FTX, generator

parser = argparse.ArgumentParser()
parser.add_argument('genome', help='genome file in FASTA format')
parser.add_argument('ftx', help='annotation in FTX format')
arg = parser.parse_args()

for chrom, seq, ftxs in generator(arg.genome, arg.ftx):
	for ftx in ftxs:
		tx = []
		for beg, end in ftx.exons: tx.append(seq[beg:end+1])
		tseq = ''.join(tx)
		print(f'>{ftx}')
		for i in range(0, len(tseq), 80):
			print(tseq[i:i+80])
