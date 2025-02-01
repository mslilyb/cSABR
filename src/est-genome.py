import argparse
import gzip
from multiprocessing import Pool
import os
import sys

from toolbox import FTX, readfasta

def run(cli, arg):
	if arg.verbose: print(cli, file=sys.stderr)
	os.system(cli)

def run_est_genome(x):
	arg, tid, rmap = x
	with open(f'{arg.build}/{tid}.ftx', 'w') as ofp:
		for i, (name, seq) in enumerate(readfasta(arg.reads)):
			if i % arg.threads != tid: continue
			gfa = f'{arg.build}/{tid}.gen.fa'
			efa = f'{arg.build}/{tid}.est.fa'
			out = f'{arg.build}/{tid}.out'
			with open(efa, 'w') as fp: print(f'>{name}', seq, sep='\n', file=fp)
			chrom, beg, end = rmap[name]
			run(f'blastdbcmd -db {arg.build}/genome.fa -entry {chrom} -range {beg}-{end} > {gfa}', arg)
			run(f'est2genome -genomesequence {gfa} -estsequence {efa} -outfile {out} 2>/dev/null', arg)
			exons = []
			strand = None
			with open(out) as fp:
				for line in fp:
					if line.startswith('Exon'):
						e, s, p, gb, ge, cx, rb, re, rs = line.split()
						strand = rs[1]
						exons.append((int(gb) -1, int(ge) -1))
			ftx = FTX(chrom, f'{i}', strand, exons, '')
			print(f'{name}~{ftx}', file=ofp)

if __name__ == '__main__':

	# CLI
	parser = argparse.ArgumentParser(description=f'threaded est2genome')
	parser.add_argument('genome', help='genome file in FASTA format')
	parser.add_argument('reads', help='reads file in FASTA format')
	parser.add_argument('-x', '--extra', type=int, default=10000,
		help='extra sequence flanking guide HSPs [%(default)i]')
	parser.add_argument('-t', '--threads', type=int, default=1,
		help='number of threads [%(default)i]')
	parser.add_argument('-b', '--build', default='temp',
		help='build directory for temp files [%(default)s]')
	parser.add_argument('-v', '--verbose', action='store_true',
		help='report diagnostic messages')
	arg = parser.parse_args()

	# PART 1: run blast to match read to chromosomal region
	os.system(f'mkdir -p {arg.build}')
	os.system(f'cp {arg.genome} {arg.build}/genome.fa')
	os.system(f'gunzip -c {arg.reads} > {arg.build}/reads.fa')
	run(f'cd {arg.build} ; makeblastdb -dbtype nucl -in genome.fa -parse_seqids > /dev/null', arg)
	run(f'blastn -db {arg.build}/genome.fa -query {arg.build}/reads.fa -outfmt 6 -num_threads {arg.threads} -evalue 1e-10 -dust no > {arg.build}/blastn.txt', arg)
	glen = {name:len(seq) for name, seq in readfasta(arg.genome)}
	readmap = {} # genome position
	offset = {}  # regional left offset
	with open(f'{arg.build}/blastn.txt') as fp:
		for line in fp:
			q, s, pct, al, mm, go, qb, qe, sb, se, ev, bs = line.split()
			if s not in readmap:
				beg, end = int(sb), int(sb)
				if beg > end: beg, end = end, beg
				beg -= arg.extra
				if beg < 1: beg = 1
				end += arg.extra
				if end > glen[s]: end = glen[s]
				readmap[q] = (s, beg, end)
				offset[q] = beg - 1

	# PART 2: run est2genome in a thread pool
	workers = [(arg, i, readmap) for i in range(arg.threads)]
	with Pool(arg.threads) as p: p.map(run_est_genome, workers)

	# PART 3: repair coordinates to make final ftx
	fps = [open(f'{arg.build}/{i}.ftx') for i in range(arg.threads)]
	while True:
		aligns = []
		for i in range(arg.threads): aligns.append(fps[i].readline())
		if aligns[0] == '': break
		for align in aligns:
			if align == '': break
			rtx, gtx = align.split('~')
			rftx = FTX.parse(rtx)
			gftx = FTX.parse(gtx)
			o = offset[f'{rftx}']
			new_exons = [(beg+o, end+o) for beg, end in gftx.exons]
			gftx.exons = new_exons
			print(f'{rftx}\t{gftx}', end='')
