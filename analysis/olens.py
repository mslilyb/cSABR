import files
import glob
import statistics
import sys

direc = sys.argv[1]

for file in sorted(glob.glob(f'{direc}/*.csv*')):
	title = True
	overhangs = {}
	threeps = {}
	fiveps = {}
	equals = {}
	ol_ind = None
	prec_ind = None
	t_ind = None
	ol_max = 0

	with files.getfp(file) as fp:
		for line in fp:
			entry = line.rstrip().split(',')
			if title:
				title = False
				ol_ind = entry.index('oh_len')
				prec_ind = entry.index('pres')
				t_ind = entry.index('oh_type')
				continue

			olen = int(entry[ol_ind])
			if olen > ol_max:
				ol_max = olen
			otype = entry[t_ind]
			prec = float(entry[prec_ind])

			if olen not in overhangs:
				overhangs[olen] = []

			overhangs[olen].append(prec)

			if otype == 'threep':
				if olen not in threeps:
					threeps[olen] = []

				threeps[olen].append(prec)

			elif otype == 'fivep':
				if olen not in fiveps:
					fiveps[olen] = []

				fiveps[olen].append(prec)

			elif otype == 'equal':
				if olen not in equals:
					equals[olen] = []

				equals[olen].append(prec)

		for i in range(ol_max):
			in_all = i in overhangs
			in_threep = i in threeps
			in_fivep = i in fiveps
			in_equal = i in equals

			if in_all:
				print(f'all,{i},{statistics.mean(overhangs[i])},{statistics.stdev(overhangs[i])},{len(overhangs[i])}')

			if in_threep:
				print(f'threep,{i},{statistics.mean(threeps[i])},{statistics.stdev(threeps[i])},{len(threeps[i])}')

			if in_fivep:
				print(f'fivep,{i},{statistics.mean(fiveps[i])},{statistics.stdev(fiveps[i])},{len(fiveps[i])}')

			if in_equal:
				print(f'equal,{i},{statistics.mean(equals[i])},{statistics.stdev(equals[i])},{len(equals[i])}')
