import files
import sys

file = sys.argv[1]
prestot = 0
linetot = 0

with files.getfp(file) as fp:
	for line in fp:
		pr = line.rstrip().split(',')[12]
		print(pr)