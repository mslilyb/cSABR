import files
import glob
import statistics
import sys

direc = sys.argv[1]

for file in sorted(glob.glob(f'{direc}/*.csv*')):
	title = True
	precs = []
	linetot = 0
	
	with files.getfp(file) as fp:
		for line in fp:
			if title:
				title = False
				continue

			precs.append(float(line.rstrip().split(',')[12]))
			linetot += 1

		print(f'{statistics.mean(precs)},{statistics.stdev(precs)},{statistics.median(precs)},{linetot}')