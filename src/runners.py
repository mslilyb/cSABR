from abc import ABC, abstractmethod
import argparse
import os
import watchdogs
import toolbox

#############
# CONSTANTS #
#############

GENOMEFILE = "genome.fa"
FTXFILE = "genome.ftx"
READSFILE = "reads.fa.gz"


# List of all programs to be used in the bakeoff
BAKEPROGS = {
	"bbmap": "sifs/bbmap.sif in={reads} ref={genome} nodisk=t threads={thr} out={out}",
	"bowtie2": None,
	#"bwa",
	"gem3-mapper": None,
	"gmap": None,
	"hisat2": None,
	"magicblast": None,
	"minimap2": None,
	"pblat": None,
	"segemehl": None,
	"star": None,
	"subread": None,
	#"tophat"
}

"""
class Program(ABC):
	Basic representation of a bakeoff program

	@abstractmethod
	def __repr__(self):
		pass

	@property
	@abstractmethod
	def cli(self):
		pass

	@cli.setter
	@abstractmethod
	def cli(self):
		pass

	def __str__(self):
		return f'{self.__repr__()}: {self._cli}'

class bbmap(Program):
	def __init__(self, cli = None):
		self.cli = cli

	def __repr__(self):
		return "bbmap"

	@property
	def cli(self):
		return self._cli

	@cli.setter
	def cli(self):
		self._cli = ''
""" #unsure about this, trying just a dict for now.


class Program:
	"""represents a program?"""
	def __init__(self, name, cli):
		self.name = name
		self.cli = cli
		#self.opts = opts

	# Stringify the program
	def __str__(self):
		return f'{self._name}: {self._cli}'

	# Getters and Setters
	@property
	def name(self):
		return self._name
	
	@name.setter
	def name(self, name):
		self._name = name


	@property
	def cli(self):
		return self._cli
	
	@cli.setter
	def cli(self, cli):
		#self._cli = cli.format(reads=READSFILE, thr=opts.thread)
		self._cli = cli

class Run:
	"""
	Represents a single run of the bakeoff?

	Has the following parameters:
	Programs: A list of objects of time Program to be used
	Method that runs it?
	Place for options from the command line?
	"""

	def __init__(self, Programs: list, Arguments: argparse.Namespace):
		"""Generator function for Run class"""
		self.Arguments = Arguments
		self.Programs = Programs
		self.info = None

	# Getters and Setters
	@property
	def Programs(self):
		return self._Programs

	@Programs.setter
	def Programs(self, Programs, Arguments):
		self._Programs = []
		for prog in Programs:
			self._Programs.append(Program(prog, BAKEPROGS[prog], Arguments))

	@property
	def Arguments(self):
		return self._Arguments
	
	@Arguments.setter
	def Arguments(self, Arguments):
		self._Arguments = Arguments

	# 'Private' methods
	def _run(self):
		pass
		
	def execute():
		for prog in self._Programs:	
			continue
		pass
	def show(self):
		print("Bakeoff Run")
		print("Arguments Selected:")
		for arg in vars(self._Arguments):
			print(f'{arg}: {getattr(self._Arguments, arg)}')
		print("Programs in Use:")
		for prog in self._Programs:
			print(prog.name)
		

# THIS IS FOR DEBUGGING
parser = argparse.ArgumentParser(description=f'python3 implementation of \
	bakeoff control.')

parser.add_argument('programs', default='all', nargs='*', \
	metavar='<programs>', help='Specify desired programs to use in bakeoff.\
	 Default behavior is to use all of them.')

# Options
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


run = Run(["bbmap"],args)
prog = Program("bbmap", BAKEPROGS["bbmap"])
print(prog)
run.show()
