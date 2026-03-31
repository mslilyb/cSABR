import os
import sys
import korflab

if len(sys.argv) != 3: sys.exit(f'usage: {sys.argv[0]} <fasta> <gff3>')
if len(sys.argv) != 4: tag = 'mRNA'
else: tag = 'transcript'
if not os.path.exists('genome.db'):
    korflab.create_database('genome.db', sys.argv[1], sys.argv[2],
        commit_every=100_000, verbose=True)

exons = {}
for gene in korflab.get_genes('genome.db', tx_tag=tag):#, tx_tag='transcript'):
    for tx in gene.transcripts:
        for f in tx.cdss[1:-1]:
            length = f.end - f.beg + 1
            sig = (f'{f.seqid}:{f.beg}-{f.end}{f.strand}', length)
            if sig not in exons: exons[sig] = 0
            exons[sig] += 1

for (coor, length), n in exons.items():
    print(coor, length, n)