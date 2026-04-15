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
parser.add_argument("-c", action='store_true', help='c_elegans')
parser.add_argument("-u", action='store_true', help='human')
parser.add_argument("-d", action='store_true', help='d_melanogaster')
parser.add_argument("-y", action='store_true', help='s_cere')
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

data = None
random = False
if args.c:
	data = '~/DATA/downloaded/c_elegans/c_elegans.PRJNA275000.WS282.genomic.fa.gz ~/DATA/generated/s_cere.ftx.gz'
elif args.u:
	data = '~/DATA/downloaded/h_sapiens/GRCh38.primary_assembly.genome.fa.gz ~/DATA/generated/h_sapiens.ftx.gz'
elif args.d:
	data = '~/DATA/downloaded/d_melanogaster/ncbi_dataset/data/GCF_000001215.4/GCF_000001215.4_Release_6_plus_ISO1_MT_genomic.fna ~/DATA/generated/d_melo.ftx.gz'
elif args.y:
	data = '~/DATA/downloaded/s_cerevisiae/ncbi_dataset/data/GCF_000146045.2/GCF_000146045.2_R64_genomic.fna ~/DATA/generated/s_cere.ftx.gz'
else:
	random = True
if args.cleanup:
	for child in start_dir.iterdir():
		if child.is_dir() and not os.path.islink(child):
			rmtree(child)
	sys.exit()
# Gen sim.
for seed in range(args.sstart, args.seed):
	if not random:
		break
	if args.simgenes:
		os.mkdir(f'{seed:03d}')
		subprocess.run(f'python3 ~/Code/cSABR/src/shuffledgensim.py {seed:03d}/{seed:03d} --double --seed {seed}', shell=True)
		continue

	subprocess.run(f'~/Code/cSABR/pb2 {seed:03d}/{seed:03d}.fa {seed:03d}/{seed:03d}.ftx {seed:03d} -{flags}{seed}', shell=True)
# Species 2: S. cerevisiae

for seed in range(args.sstart, args.seed):
	if args.simgenes or random:
		sys.exit("no")

	subprocess.run(f'~/Code/cSABR/pb2 {data} {seed:03d} -{flags}{seed}', shell=True)
