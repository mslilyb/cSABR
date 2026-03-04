from files import getfp
import sys

def parse_resultline(ftxline):
	gtruth, output = ftxline.split()
	
	expected = gtruth.split('|')[3].split(',')
	estrand = gtruth[-1]
	
	if output != 'None':
		observed = output.split('|')[3].split(',')
		ostrand = output.split('|')[2]
	else:
		observed = output
		ostrand = None
	return expected, estrand, observed, ostrand


expfiles = sys.argv[1:]
i = 0
prog_res = {}

for expfile in expfiles:
	coords = []
	pname = expfile.split('/')[-1].split('.')[0]
	prog_res[pname] = {'coords': [], 'perfects': 0}
	with getfp(expfile) as efp:
		casetot = {'five': 0, 'three': 0, 'innerfive': 0, 'innerthree': 0,'ungap': 0, 'equal': 0}
		casemiss = {'five': 0, 'three': 0, 'innerfive': 0, 'innerthree': 0, 'ungap': 0, 'equal': 0}
		strandmiss = {'+': 0, '-': 0}
		strandtot = {'+': 0, '-': 0}
		total = 0

		for line in efp:
			perfect = True
			isinner = False
			isfive = False
			isthree = False
			overhang = 0
			fivelen = 0
			threelen = 0
			case = ''

			exp, estr, obs, ostr = parse_resultline(line.rstrip())

			# Determine case

			if len(exp) < 2:
				case = 'ungap'

			else:
				fivelen = abs(int(exp[0][0]) - int(exp[0][1]))
				threelen = abs(int(exp[1][0]) - int(exp[-1][1]))


			if fivelen > threelen:
				isthree = True
				case = 'three'
				overhang = threelen	
			
			elif threelen > fivelen:
				isfive = True
				case = 'five'
				overhang = fivelen

			if len(exp) > 2:
				case = 'inner' + case

			print(case)
			i += 1

			if i > 60:
				break

categories = ['progname', 'raw_error', 'three_prime', 'thpr_avg_overhang', 'five_prime', 'fipr_avg_overhang', 'plus_str_error', 'minus_strand_error']