import os
import sys

#############
# CONSTANTS #
#############

COMPLEMENT = str.maketrans('ACGTRYMKWSBDHV', 'TGCAYRKMWSVHDB')

#############
# FUNCTIONS #
#############

# Function that returns the reverse complement of input DNA. Returns a string.
def anti(dna):
	"""reverse-complements a string"""
	return dna.translate(COMPLEMENT)[::-1]


def run(cli, f = sys.stderr):
	if f is not None:
		print("Now running:", cli, file = f)
	return os.system(cli)