import files
import glob
import statistics
import sys

direc = sys.argv[1]

for file in sorted(glob.glob(f'{direc}/*.csv*')):
	title = True
	ies = {}
	threeps = {}
	fiveps = {}
	equals = {}
	case_ind = None
	ielen_ind = None
	ie_max = 0
	prec_ind = None
	t_ind = None

	with files.getfp(file) as fp:
		for line in fp:
			entry = line.rstrip().split(',')
			if title:
				title = False
				case_ind = entry.index('case')
				ielen_ind = entry.index('ie_size')
				prec_ind = entry.index('pres')
				t_ind = entry.index('oh_type')
				continue


			case = entry[case_ind]

			if case != 'internal':
				continue

			ielen = int(entry[ielen_ind])
			if ielen > ie_max:
				ie_max = ielen

			prec = float(entry[prec_ind])
			typ = entry[t_ind]

			if ielen not in ies:
				ies[ielen] = []

			ies[ielen].append(prec)

			if typ == 'threep':
				if ielen not in threeps:
					threeps[ielen] = []

				threeps[ielen].append(prec)

			elif typ == 'fivep':
				if ielen not in fiveps:
					fiveps[ielen] = []

				fiveps[ielen].append(prec)

			elif typ == 'equal':
				if ielen not in equals:
					equals[ielen] = []

				equals[ielen].append(prec)

		for i in range(ie_max):
			if i in ies:
				print(f'all,{i},{statistics.mean(ies[i])},{statistics.stdev(ies[i])},{len(ies[i])}')
			if i in threeps:
				print(f'all,{i},{statistics.mean(threeps[i])},{statistics.stdev(threeps[i])},{len(threeps[i])}')
			if i in fiveps:
				print(f'all,{i},{statistics.mean(fiveps[i])},{statistics.stdev(fiveps[i])},{len(fiveps[i])}')
			if i in equals:
				print(f'all,{i},{statistics.mean(equals[i])},{statistics.stdev(equals[i])},{len(equals[i])}')