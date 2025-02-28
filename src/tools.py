
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