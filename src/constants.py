import os
"""
Constants for use in bakefoff script. Should be in same directory as other
parts of the source code.

While perhaps overwrought, the philosophy is simple: centralize certain aspects
of the code that may change later. Instead of hunting through the sourcecode for
where certain values or options may be, anyone can simply refer to this file and
edit the options/values here, with full confidence that the changes will be
reflected through the rest of the code. 

Constant names should be painfully descriptive to maintain code readability.
str.format() is used for the ability to *name* fields, which I believe increases
readability as well.
"""
# FUNCTIONS

# Maps /src. Not sure if I want this here, it makes less sense than in main.
def _mapsrc():
	path = os.path.abspath(__file__)
	path = path.split("/")[:-1]
	path = "/".join(path) + "/src"
	return path

# CONSTANTS

# Path to src directory. Still not sure I want this.
_SRCPATH = "to be replaced :o"

# List of all programs to be used in bakeoff.
BAKEPROGS = [
	"bbmap",
	"blat",
	"bowtie2",
	"bwa",
	"gem3-mapper",
	"gmap",
	"hisat2",
	"magicblast",
	"minimap2",
	"pblat",
	"segemehl",
	"star",
	"subread",
	"tophat"
]

# Allowable operating systems. Required for Conda and time compatibility. 
# Hoping to deprecate time with a python module. Time yet to be tested on Darwin.
TIMER = {
	"Linux": '/usr/bin/time -v ',
	"Darwin": '/usr/bin/time -l '
}

# Filename constants
GENOMEFILE = "genome.fa"
FTXFILE = "genome.ftx"
READSFILE = "reads.fa.gz"

# Internal source code path constants. Used for IPC between scripts. Will be deprecated
# once read-aligner and read-simulator are converted to modules.
ALIGNERCMD = "python3 {src}/run-aligner.py {dna} {bdir}/{reads}"
SIMULATORCMD = "python3 {src}/read-simulator.py --double {dna} {ftx}"

# CLI Options. Used to add flags/options to internal IPC commands. Will be deprectated
# once read-aligner and read-simulator are converted to modules.
OPTS = {
	'ENABLE_DEBUG_MODE': " --debug",
	'ENABLE_TESTING_MODE': " --samplegenes 0.1 --samplereads 0.1",
	'SET_SEED': " --seed {seed}",
	'SET_THREADS': " --threads {pcount}"
}