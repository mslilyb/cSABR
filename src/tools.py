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

def progressbar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', pend = '\r'):
	percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
	filledLength = int(length * iteration // total)
	bar = fill * filledLength + '-' * (length - filledLength)
	print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = pend)
	# Print New Line on Complete
	if iteration == total: 
		print()

def run(cli, f = sys.stderr):
	if f is not None:
		print("Now running:", cli, file = f)
	return os.system(cli)