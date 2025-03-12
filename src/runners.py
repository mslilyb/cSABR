from abc import ABC, abstractmethod
import argparse
from copy import deepcopy
import files
import json
import os
import sys
import watchdogs
import toolbox

#############
# CONSTANTS #
#############

GENOMEFILE = "genome.fa"
FTXFILE = "genome.ftx"
READSFILE = "reads.fa.gz"


# List of all programs to be used in the bakeoff
configfp = open("/home/alrescha/Code/cSABR/src/0config.json")
BAKEPROGS = json.load(configfp)

class Program:
	def __init__(self, name, cli, init, reqs):
		self.name = name
		self.cli = cli
		self._checks = {
			'is_formatted': self._formatself,
			'is_initialized': self.initialize
		}

		self._status = {
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

		
		
	def __str__(self):
		return f'Name: {self.name}\ncli: {self.cli}\ninits: {self.init}\nAdditional Requirements: {self.reqs}'

	def __iter__(self):
		"""
		Functions essentially as 'objtodict()' if called via built-in dict() function.
		Ex: dict(someprogram)
		"""
		yield 'name', self.name
		yield 'cli', self.cli
		yield 'init', self.init
		yield 'reqs', self.reqs

	def _execute(self, cmd):
		for check in self._checks:
			self._checks[check]()
		result = tools.run(cmd)

	def _formatself(self, direc: str, threads: int):
		if self._status['formatted'] == True:
			return

		hasfasta = self._extras['fasta']
		hasfastq = self._extras['fastq']

		if 'need_format' not in self.init.keys():
			self.cli = '{fasta}{fastq}' + self.cli

		elif hasfastq and not hasfasta:
			self.cli = '{fasta}' + self.cli
			
		elif hasfasta and not fastq:
			self.cli = '{fastq}' + self.cli

		self.cli = self.cli.format(odir=direc, genome=GENOMEFILE, reads=READSFILE, thr=threads,
			fasta=hasfasta if hasfasta else "", fastq=hasfastq if hasfastq else "")

		if not self._status['has_init']:
			return

		if 'file_exists' in self.init.keys():
			for file, fix in self.init['file_exists']:
				formattedfile = file.format(genome=GENOMEFILE)
				formattedfix = fix.format(odir=direc, genome=GENOMEFILE)
				self.init['file_exists'][file] = fixformat
				self.init['file_exists'][formattedfile] = self.init['file_exists'].pop(file)

		self._status['formatted'] = True

	def dicttoobj(self, dic):
		self.name = dic['name']
		self.cli = dic['cli']
		self.init = dic['init']
		self.reqs = dic['reqs']

	def initialize(self, direc: str, threads: int):
		# Ensure all strings are formatted
		self._checks['is_formatted'](direc, threads)

		# Check if initialized
		if self._status['initialized']:
			return

		# If not initialized, check if any initializations exist to be run
		if not self._status['has_init']:
			self._status['initialized'] = True
			return

		# Now run initializations

		# Create required files
		if 'file_exists' in self.init.keys():
			for file, fix in self.init['file_exists']:
				if not os.path.exists(f'{direc}/{file}'):
					self._execute(fix)

		# Change format of reads file
		if 'need_format' in initdict.keys():
			if initdict['need_format'] == 'fasta':
				self._extras['fasta'] = files.needfasta(READSFILE)
			if initdict['need_format'] == 'fastq':
				self._extras['fastq'] = files.needfastq(READSFILE)

		self._status['initialized'] = True

class Run:
	"""
	Represents a single run of the bakeoff?

	"""

	def __init__(self, Arguments: argparse.Namespace):
		"""Generator function for Run class"""
		self.Arguments = Arguments
		self._Programs = {}
		self.status = {
			'setup_done': False,
		}

		self._checks = {
			'setup': self.setup
		}

	# 'Private' methods
	def _makeprogs(self):
		if self.Arguments.programs == 'all':
			plist = BAKEPROGS.keys()
		else:
			plist = self.Arguments.programs
		
		for p in plist:
			newprog = Program(None, None, None, None)
			newprog.dicttoobj(BAKEPROGS[p])
			newprog.initialize(self.Arguments.dir, self.Arguments.processors)
			self._Programs[p] = newprog


	def do_run(self):
		self._checks['setup']()
		for prog in self._Programs.keys():	
			self._execute(prog)

	def setup(self):
		"""
		Three things to do: Create list of programs, change clis, run inits
		"""
		if self.status['setup_done']:
			return

		print("Configuring run.", file=sys.stderr)

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

		self.show()

		

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
	run = Run(args)
	run.test()