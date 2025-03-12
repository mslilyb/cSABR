from abc import ABC, abstractmethod
import argparse
import files
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
	"bbmap": "singularity run --bind ./{odir}/mnt sifs/bbmap.sif in=/mnt/{reads} ref=/mnt/{genome} nodisk=t threads={thr} out=/mnt/tmp--bbmap",
	"bowtie2": "singularity run --bind ./{odir}/mnt sifs/bowtie2.sif -x /mnt/{genome} -U {fastq} -k 5 > /mnt/tmp--bowtie2",
	#"bwa",
	"gem3-mapper": "singularity run --bind ./{odir}/mnt sifs/gem3mapper.sif -I /mnt/{genome}.gem -i {reads} -t {thr} > /mnt/tmp--gem3-mapper",
	"gmap": "singularity run --bind ./{odir}/mnt sifs/gmap.sif {fasta} -d {genome}-gmap -D /mnt -f samse -t {thr} > /mnt/tmp--gmap",
	"hisat2": "singularity run --bind ./{odir}/mnt sifs/hisat2.sif -x /mnt/{genome} -U /mnt/{reads} -f -p {thr} > /mnt/tmp--hisat2",
	"magicblast": "singularity run --bind ./{odir}/mnt sifs/magicblast.sif -db /mnt/{genome} -query /mnt/{reads} -num_threads {thr} > /mnt/tmp--magicblast",
	"minimap2": "singularity run --bind ./{odir}/mnt sifs/minimap2.sif -ax splice /mnt/{genome} /mnt/{reads} -t {thr} > /mnt/tmp--minimap2",
	"pblat": "singularity run --bind ./{odir}/mnt sifs/pblat.sif /mnt/{genome} /mnt/{reads} -threads={thr} -out=sim4",
	"segemehl": "singularity run --bind ./{odir}/mnt sifs/segemehl.sif -i /mnt/{genome} -q /mnt/{reads} -t {thr} --splits -o /mnt/tmp--segemehl",
	"star": "singularity run --bind ./{odir}/mnt --genomeDir {genome}--star --readFilesIn {reads} --readFilesCommand 'gunzip -c' --outFileNamePrefix /mnt/tmp--STAR --runThreadN 1",
	"subread": "singularity run --bind ./{odir}/mnt -i {genome} -r {reads} -t 0 --SAMoutput --multiMapping -B 5 -T {thr} -o /mnt/tmp--subread",
	#"tophat"
}


class Program:
	def __init__(self, name, cli, init, reqs):
		self.name = name
		self.cli = cli
		if init == None:
			self.init = {}
		else:
			self.init = init
		if reqs == None:
			self.reqs = []
		else:
			self.reqs = reqs
		
	def dicttoobj(self, dic):
		self.name = dic['name']
		self.cli = dic['cli']
		self.init = dic['init']
		self.reqs = dic['reqs']

	def __str__(self):
		return f'Name: {self.name}\ncli: {self.cli}\ninits: {self.init}\nAdditional Requirements: {self.reqs}'

	def __iter__(self):
		yield 'name', self.name
		yield 'cli', self.cli
		yield 'init', self.init
		yield 'reqs', self.reqs

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
if __name__ == '__main__':
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
