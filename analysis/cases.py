import files
import glob
import statistics
import sys

direc = sys.argv[1]

for file in sorted(glob.glob(f'{direc}/*.csv*')):
	title = True
	case_ind = None
	prec_ind = None
	cases = {}

	with files.getfp(file) as fp:
		for line in fp:
			entry = line.rstrip().split(',')
			if title:
				title = False
				case_ind = entry.index('case')
				prec_ind = entry.index('pres')
				continue

			case = line.rstrip().split(',')[case_ind]

			if case not in cases:
				cases[case] = []

			cases[case].append(float(entry[prec_ind]))

		for case in cases.keys():
			print(f'{case},{statistics.mean(cases[case])},{statistics.stdev(cases[case])},{len(cases[case])}')