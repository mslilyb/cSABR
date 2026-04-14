#!/usr/bin/env python3

import argparse
import korflab
import os
from pathlib import Path
import random
from shutil import rmtree
import subprocess
import sys
"""
directory structure:
~
|--DATA
	|--results
		|--Random
			|--Cases... (for each)
		|--S. cerevisiae
		|--D. melanogaster
		|--C. elegans
		|--H. Sapiens

order
1. make the directories
then, for each species...

"""
parser = argparse.ArgumentParser()
parser.add_argument("--cleanup", action='store_true')
parser.add_argument("--developer", action='store_true')
parser.add_argument("--dry", action='store_true')
parser.add_argument("--simgenes", action='store_true')
parser.add_argument("--test", action='store_true')
parser.add_argument('--seed', type=int, default=1)
parser.add_argument("--sstart", type=int, default=0)
args = parser.parse_args()

if not args.developer:
	sys.exit()

# cases, species. Species, then cases. each case should be its own tool
#############
## TOGGLES ##
#############
emax = 50
estep = 1
emin = 5
# Species 1: Random.
start_dir = Path(".")
flags = 's'
if args.dry:
	flags = 'y' + flags
if args.test:
	flags = 't' + flags

if args.cleanup:
	for child in start_dir.iterdir():
		if child.is_dir() and not os.path.islink(child):
			rmtree(child)
	sys.exit()
# Gen sim.
for seed in range(args.sstart, args.seed):
	if args.simgenes:
		os.mkdir(f'{seed:03d}')
		subprocess.run(f'python3 ~/Code/cSABR/src/shuffledgensim.py {seed:03d}/{seed:03d} --double --seed {seed}', shell=True)
		continue

	subprocess.run(f'~/Code/cSABR/pb2 /media/sf_vboxshare/results/random/{seed:03d}/{seed:03d}.fa /media/sf_vboxshare/results/random/{seed:03d}/{seed:03d}.ftx /media/sf_vboxshare/results/random/{seed:03d} -{flags}{seed}', shell=True)
# Species 2: S. cerevisiae
'''
for seed in range(args.sstart, args.seed):
	if args.simgenes:
		sys.exit("no")

	subprocess.run(f'~/Code/cSABR/pb2 ~/DATA/downloaded/c_elegans/c_elegans.PRJNA275000.WS282.genomic.fa.gz ~/DATA/generated/s_cere.ftx.gz {seed:03d} -{flags}{seed}', shell=True)
'''