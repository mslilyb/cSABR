import logging
import os.path as path
import platform
import sys
import src.constants as bconsts
import warnings

"""
Validation tools and error handling for bakeoff scripts.

To add:
	- Some sort of shell command error handler.
	- perhaps an output checker for each aligner????

To do:
	- develop list of other common errors and exceptions.
	- enable logfile control from CLI (simulprint? verbose? silent?)
"""

# MESSAGES
_ERRORS = {
	'EXISTS': "Skipping program %s. Output file already exists.",
	'INVALID_PROG': "Skipping program %s. Program not found in bakeoff programs.",
	'NO_VALID_PROGS': "Run terminated! No valid programs remain.",
}

_HELP = {
	'MISSED_-F': "(You can enable overwriting existing output files with '-f')",
	'MISSPELLED?': "Please double-check spelling. To add programs, please wait for me to implement that ;;"
}

# Initialize Logger. (Can make config file?)
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(levelname)s: %(message)s', level= logging.INFO)

# FUNCTIONS

# Determine if all programs exist in bakeoff pipline. Wish I could pass by
# reference. Currently duplicate function with run-aligner.py, but not forever.
def verifyprograms(progs):
	for prog in progs:
		if prog not in bconsts.BAKEPROGS:
			missing = progs.pop(progs.index(prog))
			logging.error(_ERRORS['INVALID_PROG'], missing)

	if len(progs) < 1:
		logging.error(_ERRORS['NO_VALID_PROGS'])
		logging.info(_HELP['MISSPELLED?'])
		sys.exit(1)

	return progs



# Determine if any files exist already and skip them. Run when option '-f' is
# not supplied. Wish I could pass by reference. Currently duplicate function
# with run-aligner.py, but not forever.

def noverwritten(prgs, builddir):
	for prg in prgs:
		if path.isfile(builddir + "/" + prg + ".ftx.gz"):
			skip = prgs.pop(prgs.index(prg))
			logging.warning(_ERRORS['EXISTS'], skip)

	if len(prgs) < 1:
		logger.error(_ERRORS['NO_VALID_PROGS'])
		logger.info(_HELP['MISSED_-F'])
		sys.exit(1)

	return prgs