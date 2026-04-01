import korflab
import sys

genfile = sys.argv[1]

for line in korflab.getfp(genfile):
	coords, length, n = tuple(line.rstrip().split())

	if int(length) < 50:
		print(coords, length, n)
