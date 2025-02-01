import argparse
import sys

from toolbox import FTX
from grimoire.genome import Reader

parser = argparse.ArgumentParser()
parser.add_argument('fasta', help='fasta file, compressed ok')
parser.add_argument('gff', help='gff file, compressed ok')
parser.add_argument('--developer', action='store_true')
arg = parser.parse_args()

if not arg.developer:
	sys.exit('This program is not for general use.')

genome = Reader(fasta=arg.fasta, gff=arg.gff)
for chrom in genome:
	for gene in chrom.ftable.build_genes():
		if not gene.is_coding(): continue
		tx = gene.transcripts()[0] # using 1 transcript per gene
		exons = []
		for exon in tx.exons:
			exons.append( (exon.beg-1, exon.end-1) )
		ftx = FTX(chrom.name, tx.id, tx.strand, exons, '')
		print(ftx)
