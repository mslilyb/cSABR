import files
import glob
import statistics
import sys

direc = sys.argv[1]

for file in sorted(glob.glob(f'{direc}/*.csv*')):
	title = True