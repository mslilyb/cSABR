import os
import random
import sqlite3
import sys

####
# FUNCTIONS #
####
def get_fp(file):
	"""return file pointer to multiple file types"""
	if   file == '-':          return sys.stdin
	elif file.endswith('.gz'): return gzip.open(file, 'rt')
	else:                      return open(file)

def read_one_record(file):
	"""returns header, seq"""
	# the file pointer is opened, but not closed - bad
	# the sequence is stored as a string and reallocated with += - bad
	# assumes only one header, but FASTA allows multiple records - bad
	fp = open(file)
	header = next(fp).rstrip()
	seq = ''
	for line in fp:
		seq += line.rstrip()   # offensive
	return header, seq

def read_as_two_lists(file):
	"""returns two lists: headers, sequences"""
	# the headers and sequences are stored in separate lists - bad
	# all of the sequences are read into memory - wasteful
	# uses with... but assumes normal files only - short-sighted
	headers = []
	sequences = []
	with open(arg.file) as fp:
		curr_seq = ''
		for line in fp:
			if line.startswith('>'):
				headers.append(line.rstrip())
				if curr_seq != '':
					sequences.append(curr_seq)
					curr_seq = ''
			else:
				curr_seq += line.rstrip() # still offensive
		sequences.append(curr_seq)
	return headers, sequences

def read_as_list_of_tuples(file):
	"""returns a list of (header, sequence) tuples"""
	# uses the with... syntax and multiple file types - good
	# keeps (header, sequence) together as tuple - good
	# aggregates sequence as a list and then joins to make string - good
	# keeps all sequences in memory - wasteful
	with get_fp(file) as fp:
		records = []
		header = None
		seq = []
		for line in fp:
			if line.startswith('>'):
				if seq:
					records.append( (header, ''.join(seq)) )
					seq = []
				header = line.rstrip()
			else:
				seq.append(line.rstrip())
		records.append( (header, ''.join(seq)) )
	return records

def return_tuples(fp):
	"""returns one record per call"""
	# the point of this code is to show how seek() and tell() work
	# you cannot seek() or tell() on stdin - bad
	# gzip fakes seek() and tell(), causing re-reading from the start - ugh
	# don't rewind file pointers unless you have a very good reason!
	# being too lazy to write a good parser is a bad reason
	header = fp.readline()
	seq = []
	while True:
		line = fp.readline()
		if line.startswith('>'):
			fp.seek(fp.tell() -len(line))
			return fp, header.rstrip(), ''.join(seq)
		elif line == '':
			return False, header.rstrip(), ''.join(seq)
		else:
			seq.append(line.rstrip())

def yield_tuples(file):
	"""yields one (header, seq) at a time"""
	# this is the standard way we read FASTA files
	# multiple file types are supported - good
	# minimal memory footprint - good
	with get_fp(file) as fp:
		header = None
		seqs = []
		while True:
			line = fp.readline()
			if line == '': break
			line = line.rstrip()
			if line.startswith('>'):
				if len(seqs) > 0:
					yield header, ''.join(seqs)
					header = line.rstrip()
					seqs = []
				else:
					header = line
			else:
				seqs.append(line)
		yield header, ''.join(seqs)

class FastaDatabase:
	"""class for random access to subsequences"""
	# stores ids and sequences in a SQLite database - good
	# provides random access to records - good
	# provides substring access within sequences - nice!
	# does not require FASTA file once created - cool

	def create(fasta, db):
		if os.path.exists(db): return
		con = sqlite3.connect(db)
		cur = con.cursor()
		cur.execute('CREATE TABLE sequence(name, seq)')
		con.commit()
		for header, seq in yield_tuples(fasta):
			uid = header.split()[0][1:]
			cur.execute(f'INSERT INTO sequence VALUES ("{uid}", "{seq}")')
			con.commit()

	def __init__(self, db):
		self._con = sqlite3.connect(db)
		self._cur = self._con.cursor()

	def names(self):
		res = self._cur.execute('SELECT name FROM sequence')
		return [x[0] for x in res.fetchall()]

	def get(self, uid, offset=None, length=None):
		if offset is None: return self._cur.execute(f'SELECT seq FROM sequence WHERE name="{uid}"').fetchone()[0]
		return self._cur.execute(f'SELECT substr(seq, {offset}, {length}) FROM sequence WHERE name="{uid}"').fetchone()[0]


database = sys.argv[1]
seed = sys.argv[2]

try:
	seed = int(seed)
	random.seed(seed)
except:
	print("Warning: No seed set.", file=sys.stderr)

fastarecs = FastaDatabase(database)

namelist = fastarecs.names()

for endswap in reversed(range(len(namelist))):
	swapout = namelist[endswap]
	if endswap - 1 < 0:
		swapin = 0
	else:
		swapin = random.randint(0, endswap - 1)
	namelist[endswap] = namelist[swapin]
	namelist[swapin] = swapout
	print(f'>{namelist[endswap]}\n{fastarecs.get(namelist[endswap])}')