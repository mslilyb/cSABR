import argparse

"""
Argument parsers to use for user I/O for the SABR project.
"""

"""
bakeoff main script parser
"""
def bakeargs():
	# Required positional arguments
	parser = argparse.ArgumentParser(description=f'python3 implementation of \
		bakeoff control.')
	parser.add_argument('dna', type=str, metavar='<fasta file>', help='path \
		to genome in fasta format.')
	parser.add_argument('ftx', type=str, metavar='<ftx file>', help='path to \
		reads file in .ftx format.')
	parser.add_argument('dir', type=str, metavar='<directory>', help='name of \
		desired output directory')

	# Optional positional arguments

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

	return parser.parse_args()