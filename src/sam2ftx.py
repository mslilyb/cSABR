import argparse
import gzip
import sys

from toolbox import sam_to_ftx

parser = argparse.ArgumentParser(
	description='convert SAM - for programs run externally')
parser.add_argument('sam', help='sam file')
parser.add_argument('out', help='output file, add .gz to compress')
arg = parser.parse_args()

if   arg.out.endswith('ftx.gz'): fp = gzip.open(arg.out, 'wt')
elif arg.out.endswith('ftx'):    fp = open(arg.out, 'w')
elif arg.out == '-':             fp = sys.stdout
else: sys.exit('output should be *.ftx, *.ftx.gz, or -')

for ftx in sam_to_ftx(arg.sam): print(ftx, file=fp)

"""

This program is only intended for the rare circumstances when a program is run
outside the normal bakeoff context. An example is "dragen", which is FPGA-based
hardware.

"""
