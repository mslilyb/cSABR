import files
import glob
import math
import statistics
import sys

def findweighta(av, we):
	tot = sum(we)
	we_av = 0
	for i in range(len(av)):
		we[i] /= tot
		we_av += av[i] * we[i]
	return we_av

def findweightv(av, we, w_av):
	w_var = 0
	for i in range(len(av)):
		w_var += we[i] * (av[i] - w_av) ** 2

	return w_var

directory = sys.argv[1]
fields = sys.argv[2:]

for i in range(len(fields)):
	print(fields[i], end='')

	if i + 1 == len(fields):
		break

	print(',', end='')

print()


for file in sorted(glob.glob(f'{directory}/*.csv*')):
	fname = file.strip().split('/')[-1].split('_')[0]	
	with files.getfp(file) as fp:
		cs = {}
		avera = []
		weights = []
		for line in fp:
			#c, p, s, n = line.rstrip().split(',') for cases
			c, l, p, s, n = line.rstrip().split(',')
			avera.append(float(p))
			weights.append(int(n))
			if c not in cs:
				cs[c] = {
					'avgs': [],
					'num': []
				}

			cs[c]['avgs'].append(float(p))
			cs[c]['num'].append(int(n))

		av_precision = findweighta(avera, weights)
		av_var = findweightv(avera, weights, av_precision)

		print(fname,'precision',av_precision,math.sqrt(av_var), sep=',')
		for ca in cs.keys():
			wei_avg = findweighta(cs[ca]['avgs'], cs[ca]['num'])
			assert math.isclose(sum(cs[ca]['num']), 1.00)


			wei_var = findweightv(cs[ca]['avgs'], cs[ca]['num'], wei_avg)
			if wei_avg > 1:
				wei_avg = 1.00
				wei_var = 0

			print(fname, ca, wei_avg, math.sqrt(wei_var), sep=',')



