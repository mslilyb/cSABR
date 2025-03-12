import argparse
from copy import deepcopy
import json
import os
from runners import Program
import sys
from types import SimpleNamespace as Namespace

OPTIONS = ['init', 'reqs']
INITS = ['file_exists', 'need_format', 'other']

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
"""
This program creates and curates a configuration file for the larger bakeoff. The format is .json. Interactive mode is default. More to come?
"""
def prompt():
	print('Choice:', end=' ')

def listopts(kind):
	for i, o in enumerate(kind):
		print(f'{i + 1}: {o}')

def addprog():
	p = Program(None, None, None, None)
	print('Input name of Program:', end=' ')
	p.name = input()
	print('Provide cli. Replace files with .format() fields:')
	p.cli = input()
	while True:
		print('Select any additional options, or type "done" to finish.')
		print('Options:')
		listopts(OPTIONS)
		prompt()
		selection = input()
		if selection == 'done':
			print('Finalizing Program:')
			print(p.__str__())
			break

		if selection == '1':
			while True:
				print('Specify any additional initializations. Type "done" to finish:')
				listopts(INITS)
				prompt()
				selection = input()
				if selection == 'done':
					break

				try:
					p.init[INITS[int(selection) - 1]] = None

				except:
					print('ERROR: provide option by inputting number')
					print()
				
				if selection == '1':
					print('File name required:', end=' ')
					file = input()
					print('cmd to run if not found:')
					filecmd = input()
					p.init['file_exists'] = {file: filecmd}

				if selection == '2':
					print('File format required:', end= ' ')

					form = input()

					p.init['need_format'] = form.lower()

		if selection == '2':
			while True:
				print('Specify other requirements. Type "done" to finish:', end=' ')
				req = input()

				if req == 'done':
					break

				p.reqs.append(req)
	return p


# Main parser

parser = argparse.ArgumentParser(description='create .json configuration file with run details for bakeoff programs')
parser.add_argument('json', type=str, metavar='<file>', help='config file in .json format')
parser.add_argument('--readin', action = 'store_true', help='Read in details from command line.')
parser.add_argument('-o', '--overwrite', action='store_true', help='overwrite any existing config file. default behavior is to append')

args = parser.parse_args()


if args.overwrite or not os.path.exists(args.json):
	try:
		open(args.json, 'x')
	except:
		print(f'File {args.json} exists. Overwriting')
		os.unlink(args.json)
		open(args.json, 'x')
	finally:
		progs = {}
else:
	fp = open(args.json)
	#progs = json.load(fp, object_hook=lambda d: Namespace(**d))
	progs = json.load(fp)
	fp.close()


while True:
	newpro = addprog()
	progs[newpro.name] = dict(newpro)
	print()
	print('Add additional programs? Type "done" to finish:', end=' ')
	choice = input()

	if choice == 'done':
		break


print('Input succesful. Writing config file for the following programs:')
for pro in progs.keys():
	print(f'{pro}')

print('Writing json.')

fp = open(args.json, 'wt')
json.dump(progs, fp)
