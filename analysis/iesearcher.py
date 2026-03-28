from korflab import getfp, GFF, readgff
import sys

"""
python3 script to read through and parse a gff3 file to find all the internal exons that match our criteria

Internal exons meet three criteria:
	- Start coordinate is after the gene start coordinate
	- end coordinate is before the gene start coordinate
	- total length of the exon is less than or equal to the maximum internal exon length (default = 50)


potentially interesting angles to pursue (i love being thorough!!!!!)
- what method (sequencing/alignment) was used to validate this internal exon?
- how many internal exons exist in the human genome/what is the incidence rate
- how many are validated by RNA-seq
	- what method was used to validate this internal exon?
	- for those NOT validated by RNA-seq, what aligners/methods were used to validate the other parts of the genome?

Then, run SABR on human genome data.


"""

gffile = sys.argv[1]
ielen = int(sys.argv[2])


currgene = None
found = False

for gffline in readgff(gffile):
	if gffline.type == 'gene':
		found = False
		#attribs = {att.split('=')[0]: att.split('=')[1] for att in gffline.attr.rstrip().split(';')}
		currgene = gffline

	elif gffline.type == 'exon':
		edge_exon = (gffline.beg <= currgene.beg or gffline.end >= currgene.end)
		long_exon = ((gffline.end - gffline.beg) > ielen)
		if edge_exon or long_exon:
			continue

		if not found:
			found = True
			print(currgene)

		print(gffline)

