# toolbox.py - various functions for the SABR project

import gzip
import re

###########
# General #
###########

COMPLEMENT = str.maketrans('ACGTRYMKWSBDHV', 'TGCAYRKMWSVHDB')

def anti(dna):
	"""reverse-complements a string"""
	return dna.translate(COMPLEMENT)[::-1]

def getfp(filename):
	"""returns a file pointer for reading based on file name"""
	if   filename.endswith('.gz'): return gzip.open(filename, 'rt')
	elif filename == '-':          return sys.stdin
	else:                          return open(filename)

#############
# FTX Files #
#############

class FTX:
	"""class to represent transcripts with one-line formatting"""

	def __init__(self, chrom, name, strand, exons, info):
		# sanity checks
		assert('|' not in chrom)
		assert(' ' not in chrom)
		assert('|' not in name)
		assert(' ' not in name)
		assert(strand == '+' or strand == '-')
		for beg, end in exons: assert(beg <= end)
		for i in range(len(exons) -1): assert(exons[i][0] < exons[i+1][0])

		self.chrom = chrom
		self.beg = exons[0][0]
		self.end = exons[-1][1]
		self.name = name
		self.strand = strand
		self.exons = exons
		self.info = info

	def exon_length(self, n):
		"""retrieves the exon length of an enumerated exon"""
		return self.exons[n][1] - self.exons[n][0] + 1

	def overlaps(f1, f2, strand_sensitive=True):
		"""tests if two ftx objects overlap each other"""
		if f1.chrom != f2.chrom: return False
		if f1.strand != f2.strand and strand_sensitive: return False
		if f1.beg <= f2.beg and f1.end >= f2.beg: return True
		return False

	def matches(f1, f2):
		"""true if all exons are identical"""
		if len(f1.exons) != len(f2.exons): return False
		for (b1, e1), (b2, e2) in zip(f1.exons, f2.exons):
			if b1 != b2: return False
			if e1 != e2: return False
		return True

	def similar(f1, f2):
		if f1.overlaps(f2) and f1.distance(f2) <= 0.5: return True
		return False

	def distance(f1, f2):
		"""distance (0-1) between 2 ftx objects where 0 is identity"""

		# check for identity, zero distance
		if len(f1.exons) == len(f2.exons):
			identical = True
			for (b1, e1), (b2, e2) in zip(f1.exons, f2.exons):
				if b1 != b2:
					identical = False
					break
				if e1 != e2:
					identical = False
					break
			if identical: return 0

		# examine shared coordinates, non-zero distance
		f1b = [beg for beg, end in f1.exons]
		f1e = [end for beg, end in f1.exons]
		f2b = [beg for beg, end in f2.exons]
		f2e = [end for beg, end in f2.exons]
		total = len(f1b) + len(f1e)
		shared = 0
		for beg in f1b:
			if beg in f2b: shared += 1
		for end in f1e:
			if end in f2e: shared += 1

		return (total - shared) / total

	def text(self):
		"""text-based version of ftx, 1-based"""
		estr = ','.join([f'{beg+1}-{end+1}' for beg, end in self.exons])
		return '|'.join((self.chrom, self.name, self.strand, estr, self.info))

	def __str__(self):
		"""ftx objects can stringify themselves"""
		return self.text()

	@classmethod
	def parse(self, text):
		"""returns ftx object from a string"""
		chrom, name, strand, estr, info = text.split('|', 4)
		exons = []
		for s in estr.split(','):
			beg, end = s.split('-')
			exons.append((int(beg)-1, int(end)-1))
		return FTX(chrom, name, strand, exons, info)

###########
# Genomes #
###########

def readfasta(filename):
	"""generates defline, seq from fasta files"""
	name = None
	seqs = []
	fp = getfp(filename)
	while True:
		line = fp.readline()
		if line == '': break
		line = line.rstrip()
		if line.startswith('>'):
			if len(seqs) > 0:
				seq = ''.join(seqs)
				yield(name, seq)
				name = line[1:]
				seqs = []
			else:
				name = line[1:]
		else:
			seqs.append(line)
	yield(name, ''.join(seqs))
	fp.close()

def generator(fastafile, ftxfile):
	"""generates name, seq, ftx-genes from fasta and ftx files"""
	ftx_table = {}
	fp = getfp(ftxfile)
	for line in fp:
		ftx = FTX.parse(line.rstrip())
		if ftx.chrom not in ftx_table: ftx_table[ftx.chrom] = []
		ftx_table[ftx.chrom].append(ftx)
	for defline, seq in readfasta(fastafile):
		chrom = defline.split()[0]
		if chrom in ftx_table: yield chrom, seq, ftx_table[chrom]

#############
# SAM Files #
#############

class SAMbitflag:
	"""class for sam bitflags"""
	def __init__(self, val):
		i = int(val)
		b = f'{i:012b}'
		self.read_unmapped = True if b[-3] == '1' else False
		self.read_reverse_strand = True if b[-5] == '1' else False
		self.not_primary_alignment = True if b[-9] == '1' else False
		self.supplementary_alignment = True if b[-12] == '1' else False
		self.otherflags = []
		for i in (1, 2, 4, 6, 7, 8, 10, 11):
			if b[-i] == '1': self.otherflags.append(i)

def cigar_to_exons(cigar, pos):
	"""converts cigar strings to exon coorinates"""
	exons = []
	beg = 0
	end = 0
	for match in re.finditer(r'(\d+)([\D])', cigar):
		n = int(match.group(1))
		op = match.group(2)
		if   op == 'M': end += n
		elif op == '=': end += n
		elif op == 'X': end += n
		elif op == 'D': pass
		elif op == 'I': end += n
		elif op == 'S': pass
		elif op == 'H': pass
		elif op == 'N':
			exons.append((pos+beg-1, pos+end-2))
			beg = end + n
			end = beg
	exons.append((pos+beg-1, pos+end-2))
	return exons

def sam_to_ftx(filename):
	"""generates ftx objects from sam file"""
	n = 0
	with open(filename, errors='ignore') as fp:
		for line in fp:
			if line == '': break
			if line.startswith('@'): continue
			f = line.split('\t')
			qname = f[0]
			bf = SAMbitflag(f[1])
			chrom = f[2]
			pos   = int(f[3])
			cigar = f[5]

			st = '-' if bf.read_reverse_strand else '+'
			if bf.read_unmapped: continue
			if bf.otherflags:
				print(bf.otherflags)
				sys.exit('unexpected flags found, debug me')
			n += 1
			exons = cigar_to_exons(cigar, pos)
			yield FTX(chrom, str(n), st, exons, f'~{qname}')
