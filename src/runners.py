import argparse
from copy import deepcopy
import files
import json
import logging
import os
import readsim
import shutil
import sys
import watchdogs
import tools
from typing import Generator

#############
# CONSTANTS #
#############

GENOMEFILE = "genome.fa"
FTXFILE = "genome.ftx"
READSFILE = "reads.fa"


# List of all programs to be used in the bakeoff
configfp = open("src/00CONFIG.json")
BAKEPROGS = json.load(configfp)

###########
# CLASSES #
###########

###########
# PROGRAM #
###########

class Program:
	"""
	Class representing an alignment program to be used in the cSABR bakeoff pipeline.

	A program should know its own name, all of its requirements, and be able to run itself,
	reporting the results to whatever method or program invoked it.

	This is theoretically generalizable, but for now specifically is for use in cSABR.
	"""

	# Dunders
	def __init__(self, name, cli, init, reqs, direc: str, threads: int) -> None:
		"""
		Parameters
		----------
		+ name        `str`    name of program. independent of run options
		+ cli         `str`    string containing command for running the program. independent of run options
		+ init        `dict`   dictionary of initializations required to execute the Program. independent of run options
		+ reqs        `list`   currently unused??? i have ideas on using this to generalize the object
		+ direc       `str`    output directory for the bakeoff run. dependent on run options
		+ thread      `int`    number of threads/processors to be used during Program execution. dependent on run options

		Attributes
		----------
		+ _checks     `dict`   dictionary of methods used to ensure correct initialization of a Program object
		+ _status     `dict`   dictionary of boolean values to track progress of Program instantiation
		+ _extras     `dict`   dictionary of extra values needed to run a Program, used only when necessary
		"""
		self.name = name
		self.cli = cli
		self._checks = {
			'files_created': self._makereqs,
			'is_formatted': self._formatself,
			'is_initialized': self.initialize
		}

		self._status = {
			'files_created': False,
			'has_init': False,
			'has_reqs': False,
			'initialized': False,
			'formatted': False,
			'reqs_met': False

		}

		self._extras = {
			'fasta': False,
			'fastq': False
		}

		if init == None:
			self.init = {}
		else:
			self.init = init
			self._status['has_init'] = True

		if reqs == None:
			self.reqs = []
		else:
			self.reqs = reqs

		self.direc = direc
		self.threads = threads
		
		
	def __str__(self) -> str:
		"""
		Stringify a Program object, returning a string with each independent parameter on a single line.
		"""
		return f'Name: {self.name}\ncli: {self.cli}\ninits: {self.init}\nAdditional Requirements: {self.reqs}'

	def __iter__(self) -> Generator[tuple, None, None]:
		"""
		Yields independent parameters as tuples, which can be used to create dictionaries or as a generator.
		"""
		yield 'name', self.name
		yield 'cli', self.cli
		yield 'init', self.init
		yield 'reqs', self.reqs

	# Private methods
	def _formatself(self) -> None:
		"""
		Private method that converts a Program's cli and other commands from templates
		into specific commands, using run options. After calling it, a Program will be
		ready to execute.
		"""
		if self._status['formatted'] == True:
			return
		hasfasta = self._extras['fasta']
		hasfastq = self._extras['fastq']

		if 'need_format' not in self.init.keys():
			self.cli = '{fasta}{fastq}' + self.cli

		elif hasfastq and not hasfasta:
			self.cli = '{fasta}' + self.cli

		elif hasfasta and not hasfastq:
			self.cli = '{fastq}' + self.clifiles

		self.cli = self.cli.format(odir=self.direc, genome=GENOMEFILE, reads=READSFILE, thr=self.threads,
			fasta=hasfasta if hasfasta else "", fastq=hasfastq if hasfastq else "")

		if not self._status['has_init']:
			return

		if 'file_exists' in self.init:
			newdic = {}
			for file, fix in self.init['file_exists'].items():
				formattedfile = file.format(genome=GENOMEFILE)
				formattedfix = fix.format(odir=self.direc, genome=GENOMEFILE)
				newdic[formattedfile] = formattedfix
			
			self.init['file_exists'] = newdic

		self._status['formatted'] = True

	def _makereqs(self, is_dry):

		if self._status['files_created']:
			return

		# Change format of reads file
		if 'need_format' in self.init.keys():
			if self.init['need_format'] == 'fasta':
				logging.info(f'{self.name} requires fasta format files. Reformatting.')
				if not is_dry:
					self._extras['fasta'] = files.needfasta(f'{self.direc}/{READSFILE}')
			if self.init['need_format'] == 'fastq':
				logging.info(f'{self.name} requires fastq format files. Reformatting.')
				if not is_dry:
					self._extras['fastq'] = files.needfastq(f'{self.direc}/{READSFILE}')
					print(self._extras['fastq'], 'is the created file.')

		self._status['files_created'] = True

	# Public methods
	def execute(self, is_dry) -> int:
		"""
		Public method that runs a Program's cli, returning the resulting exit code.
		"""
		self._checks['is_initialized'](is_dry)
		logging.info(f'Now running: {self.name}')
		logging.info(f'cli: {self.cli}')
		if is_dry: return 0

		result = tools.run(self.cli)

		#create output files, redo to have path designation in function.
		tmpfp = self.direc + '/' + 'tmp--' + self.name #ugly.
		ftxfp = self.direc + '/' + 'ftx--' + self.name # ugly untested
		if self.name == 'pblat': #actually vomit inducing
			files.sim4file_to_ftxfile(tmpfp, ftxfp)

		else:
			files.samfile_to_ftxfile(tmpfp, ftxfp)

		# Generate final output
		files.reportalignments(READSFILE, ftxfp, self.name, self.direc)


	def fromdict(self, dic):
		self.name = dic['name']
		self.cli = dic['cli']
		self.init = dic['init']
		if self.init != {}:
			self._status['has_init'] = True
		self.reqs = dic['reqs']

	def initialize(self, is_dry):
		# Ensure all strings are formatted
		self._checks['files_created'](is_dry)
		self._checks['is_formatted']()

		# Check if initialized
		if self._status['initialized']:
			return

		# If not initialized, check if any initializations exist to be run
		if not self._status['has_init']:
			self._status['initialized'] = True
			return
			
		# Create required files
		if 'file_exists' in self.init.keys():
			for file, fix in self.init['file_exists'].items():
				if not os.path.exists(f'{self.direc}/{file}'):
					logging.info(f'Now initializing: {self.direc}/{file}')

					if is_dry: continue

					tools.run(fix, f = None)

		self._status['initialized'] = True

class Run:
	"""
	Represents a single run of the bakeoff. 
	A Run should know its user defined options, the programs that need to be used, be able to orchestrate the execution of all of its programs.
	It should track and report the progress and status of the bakeoff as it runs.

	"""

	# Dunders
	def __init__(self, Arguments: argparse.Namespace):
		"""
		Parameters
		----------
		+ Arguments    `argparse.Namespace`    Namespace object from argparse.

		Attributes
		----------
		+ _checks      `dict`   dictionary containing methods used to ensure bakeoff has been setup correctly
		+ _Programs    `dict`   dictionary containing all programs for use in bakeoff. Keys are program names, values are Program objects
		+ status       `dict`   dictionary containing boolean values tracking the status of the bakeoff. currently for setup.
		"""
		self.Arguments = Arguments
		self._Programs = {}
		self.status = {
			'setup_done': False,
			'run_done': False
		}

		self._checks = {
			'setup': self.setup,
			'ran': self.do_run
		}

	# Private methods
	def _makeprogs(self):
		if self.Arguments.programs == 'all':
			plist = BAKEPROGS.keys()
		else:
			plist = watchdogs.verifyprograms(self.Arguments.programs, BAKEPROGS)
		
		# Overwrite protection
		if self.Arguments.f == False and os.path.isdir(self.Arguments.dir):
				plist = watchdogs.noverwritten(plist, self.Arguments.dir)

		for p in plist:
			newprog = Program(None, None, None, None, None, None)
			newprog.fromdict(BAKEPROGS[p])
			newprog.threads = self.Arguments.processors
			newprog.direc = self.Arguments.dir
			newprog.initialize(self.Arguments.dry)
			self._Programs[p] = newprog

	def _makefiles(self):
		newfastap = f'{os.path.abspath(self.Arguments.dir)}/{GENOMEFILE}'
		newreadsp = f'{os.path.abspath(self.Arguments.dir)}/{READSFILE}'
		logging.info(f'Preparing {newfastap}')

		if not self.Arguments.dry:
			with files.getfp(self.Arguments.dna) as f_in:
				with open(newfastap, 'wt') as f_out:
					shutil.copyfileobj(f_in, f_out)
		
		logging.info(f'Generating {newreadsp}')
		if not self.Arguments.dry:
			sgenes = 1.0
			sreads = 1.0
			if self.Arguments.t:
				sgene = 0.1
				sreads = 0.1
			print('simulating reads')
			files.simulatereads(newfastap, self.Arguments.ftx, self.Arguments.seed, samplegenes = sgenes, samplereads = sreads, double = True, outf = newreadsp)


	# Public methods
	def do_run(self):
		self._checks['setup']()
		if self.status['run_done']:
			return
		for prog in self._Programs.values():	
			prog.execute(self.Arguments.dry)

		self.status['run_done'] = True

	def report(self):
		self._checks['ran']()
		logging.info('Reporting Run Results')
		if not self.Arguments.dry:
			readpath = f'{self.Arguments.dir}/{READSFILE}'
			targetpath = f'{self.Arguments.dir}'
			files.reportalignments(f'{self.Arguments.dir}/{READSFILE}', self.Arguments.ftx, f'')

	def setup(self):
		"""
		Three things to do: Create list of programs, change clis, run inits
		"""
		if self.status['setup_done']:
			return

		logging.info('Configuring Run.')

		self._makefiles()
		self._makeprogs()
		self.status['setup_done'] = True

	def show(self):
		self._checks['setup']()

		print("Bakeoff Run")
		print("Arguments Selected:")
		for arg in vars(self.Arguments):
			print(f'{arg}: {getattr(self.Arguments, arg)}')
		print("Programs in Use:")
		for pname, p in self._Programs.items():
			print(pname)
			print(p)

	def test(self):
		"""
		For debugging, to ensure all objects are created correctly.
		"""
		for check in self._checks:
			self._checks[check]()

		logging.info('Now showing Run')
		self.show()
		self.do_run()

		

# THIS IS FOR DEBUGGING
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description=f'python3 implementation of \
		bakeoff control.')


	parser.add_argument('programs', default='all', nargs='*', \
		metavar='<programs>', help='Specify desired programs to use in bakeoff.\
		 Default behavior is to use all of them.')

	# Options
	parser.add_argument('--dir', required=False, default='build')
	parser.add_argument('-p', '--processors', required=False, default=1, \
		type=int, metavar='<count>', help='Number of \
		processors to use for programs that support multiprocessing. Default: \
		[%(default)s]')
	parser.add_argument('-s', '--seed', required=False, default=None, \
		type=int, metavar='<random seed>', help='Random seed for \
		reproducibility. Default: [%(default)s]')

	# On/Off flags
	parser.add_argument('-t', action='store_true', help='Enable testing mode, \
		which uses only 1/10th of the gene and input files.')
	parser.add_argument('-m', '--md5', action='store_true', help='Perform md5 \
		checksums on data and *.ftx.gz files')
	parser.add_argument('-f', action='store_true', help='Force overwrite of \
		any existing files. Normal behavior is skipping them.')
	parser.add_argument('-d', action='store_true', help='Enable debug mode, \
		keeping temporary files.')
	args = parser.parse_args()


	print(args.programs)
