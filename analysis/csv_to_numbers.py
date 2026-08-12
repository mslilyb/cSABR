import argparse
from copy import deepcopy
import files
import glob
import os
import random
import sys

for file in sorted(glob.glob(f'{directory}/*.csv*')):
	title = True
	for line in files.getfp(file):
		if title:
			