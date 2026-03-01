import files
import sys
import random


ftx_file = sys.argv[1]

try:
	seed = sys.argv[2]
except:
	print("error: seed required", file=sys.stderr)
	sys.exit()
finally:
	seed = int(seed)

filelines = []

with files.getfp(ftx_file) as infp:
	filelines = infp.readlines()


for linenum in reversed(range(len(filelines))):
	swapout = filelines[linenum]

	if linenum -1 < 0:
		swapin = 0

	else:
		swapin = random.randint(0, linenum - 1)

	filelines[linenum] = filelines[swapin]
	filelines[swapin] = swapout

	print(filelines[linenum].rstrip())
