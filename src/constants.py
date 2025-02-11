import os
"""
Constants for use in bakefoff script. Should be in same directory as other
parts of the source code.
"""
def _mapsrc():
	path = os.path.abspath(__file__)
	path = path.split("/")[:-1]
	path = "/".join(path) + "/src"
	return path

# Path to src directory. If I could make this private I would.
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

# Allowable operating systems. Required for Conda workflow compatibility.
OS = [
	"Linux",
	"Darwin"
]

# Filename constants
GENOMEFILE = "genome.fa"
FTXFILE = "genome.ftx"
READSFILE = "reads.fa.gz"

# Internal source code path constants. Used for IPC between scripts.
ALIGNER = "run-aligner.py"
SIMULATOR = "read-simulator.py"

# _mapsrc() # This is a weird idea. IDK if it's necessary.