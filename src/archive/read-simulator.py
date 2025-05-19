import argparse
import random
import sys

from toolbox import FTX, generator, anti

def generate_reads(gftx, chrom, size):
	# create indexes
	dna = [] # dna positional index
	rna = [] # rna sequence
	for beg, end in gftx.exons:
		for i in range(end - beg + 1):
			coor = i + beg
			dna.append(coor)
			rna.append(chrom[coor])

	# generate reads and their ftx annotations
	for i in range(len(rna) - size + 1):
		coor = [dna[i+j] for j in range(size)]
		exons = []
		beg = coor[0]
		seen = 0
		for j in range(size -1):
			d = coor[j+1] - coor[j]
			if d > 1:
				end = beg + j -seen
				exons.append( (beg, end) )
				seen += end - beg + 1
				beg = coor[j+1]
		exons.append( (beg, beg+j -seen +1) )
		rftx = FTX(gftx.chrom, gftx.name, gftx.strand, exons, 'r')
		read = ''.join([chrom[beg:end+1] for beg, end in exons])

		yield rftx, read

parser = argparse.ArgumentParser()
parser.add_argument('fasta', help='fasta file')
parser.add_argument('ftx', help='ftx file')
parser.add_argument('--readlength', type=int, default=100, metavar='<int>',
	help='[%(default)i]')
parser.add_argument('--samplegenes', type=float, default=1.0, metavar='<p>',
	help='downsample genes [%(default).3f]')
parser.add_argument('--samplereads', type=float, default=1.0, metavar='<p>',
	help='downsample reads [%(default).3f]')
parser.add_argument('--seed', type=int, default=0, metavar='<int>',
	help='set random seed')
parser.add_argument('--double', action='store_true',
	help='produce reads from both strands')
arg = parser.parse_args()

if arg.seed != 0: random.seed(arg.seed)

genes = 0
reads = 0
bases = 0

for cname, cseq, gtfxs in generator(arg.fasta, arg.ftx):
	for gftx in gtfxs:
		if random.random() > arg.samplegenes: continue
		genes += 1
		for rftx, rseq in generate_reads(gftx, cseq, arg.readlength):
			if random.random() < arg.samplereads:
				print('>', rftx, '+', sep='')
				print(rseq)
				reads += 1
				bases += arg.readlength
			if arg.double and random.random() < arg.samplereads:
				rseq = anti(rseq)
				print('>', rftx, '-', sep='')
				print(rseq)
				reads += 1
				bases += arg.readlength

print(f'genes: {genes}', f'reads: {reads}', f'bases: {bases}',
	sep='\n', file=sys.stderr)
