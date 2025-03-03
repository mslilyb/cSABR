import src.watchdogs
import toolbox

#############
# CONSTANTS #
#############

# List of all programs to be used in the bakeoff
BAKEPROGS = {
	"bbmap": "bbmap.sh in={reads} ref={genome} nodisk=t threads={thr} out={out}",
	"bowtie2": ,
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