import sys
import files

revfile = sys.argv[1]
outfile = "revreads.fa"

with files.getfp(revfile) as fp:
	with open(outfile, 'a') as wfp:
		seqline = None
		defline = None
		for line in fp:
			if not line.startswith('>'):
				seqline = line.strip()
			else:
				defline = line.strip()
				if defline is not None and seqline is not None:
					print(defline, file=wfp)
					print(seqline, file=wfp)
					defline = None
					seqline = None