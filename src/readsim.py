import argparse
import random
import sys

from toolbox import FTX, generator, anti

#############
# FUNCTIONS #
#############

#
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

# Read simulator.Returns nothing, instead printing the output, default to stdout
# but a different output file can be specified. Reports run information after
# completing the simulation to stderr. Do I like this?
def simreads(fasta, ftx, outfile=None, rlen = 100, gsample=1.0, rsample=1.0, seed=None, double=True):
	genes = 0
	reads = 0
	bases = 0
	if seed != None:
		random.seed(seed)
	if outfile != None:
		out = open(outfile, 'w')
	else:
		out = sys.stdout
	for cname, cseq, gtfxs in generator(fasta, ftx):
		for gftx in gtfxs:
			if random.random() > gsample:
				continue
			genes += 1

			for rftx, rseq in generate_reads(gftx, cseq, rlen):
				if random.random() <= rsample:
					print('>', rftx, '+', sep='', file=out)
					print(rseq, file=out)
					reads += 1
					bases += rlen
				if double and random.random() <= rsample:
					rseq = anti(rseq)
					print('>', rftx, '-', sep='', file=out)
					print(rseq)
					reads += 1
					bases += rlen

	print(f'genes: {genes}', f'reads: {reads}', f'bases: {bases}',
	sep='\n', file=sys.stderr)

	if outfile != None:
		out.close()

	return None


##########
# TESTER #
##########

if __name__ == '__main__':
	simreads(sys.argv[1], sys.argv[2], gsample = 0.1, rsample = 0.1, seed = 1)