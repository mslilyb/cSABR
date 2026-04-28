#!/usr/bin/env python3
import files
import sys
import random

# explaining here what I would like to do so that i can once again arrange my thoughts
"""
The .ftx file format was designed to facilitate simple data storage and handling for the SABR project, however
its utility means that it will likely outrange it in usage. To that end, and to better exhibit the virtue of 
'one tool, one purpose', this script and collection of modules will seek to process FTXs and parse their data
to be used in downstream analysis. By making the steps discreet, more efficient analysis can be carried out.

For now this module will likely only concern itself with the SABR project and what it is interested in. In future,
it may be useful as a diagnostic or part of a larger workflow.

Current goals:
- line by line, understand the case and results. Case is determined by ground truth, results through comparison
- generate output files, each containing the results for the isolated aspect of interest. As of right now, that includes
  unspliced, spliced, anad internal cases.

thought: need to keep track of names and it is enough for now to realize this: that you need to sleep earlier and get to campus with more time before having to go home to feed nori.
"""
def accfinder(ec, gc, cs):
  errtyp = ''
  shift = None

  if len(gc) < len(ec):
    errtyp += 'false_splice'
    if cs == 'unspliced': return errtyp, coverage(ec, gc)
  
  elif len(gc) > len(ec):
    errtyp += 'missed_splice'

  else:
    errtyp += 'n/a'

  return errtyp, coverage(ec, gc)

  # to add later LATER DAMMIT: is it truncated or shifted? In what direction?

def casefinder(coords, rl):
  if len(coords) < 2:
    return "unspliced"

  elif len(coords) == 2:
    return "spliced"

  elif lenfinder(coords[0]) + lenfinder(coords[1]) > rl:
    return "spliced"

  elif len(coords) > 2:
    return "internal"

def coordfinder(pair):
  return int(pair.split('-')[0]), int(pair.split('-')[1])

def coverage(ex, gt):
  hits = 0
  totlen = 0

  for g in gt:
    g_beg, g_end = coordfinder(g)
    totlen += lenfinder(g)

    for e in ex:
      e_beg, e_end = coordfinder(e)

      for i in range(g_beg, g_end + 1):
        if i >= e_beg and i <= e_end:
          hits += 1

  return hits / totlen

def gapfinder(coords):
  if lenfinder(coords[-1]) > lenfinder(coords[0]):
    return "fivep", lenfinder(coords[1])
  elif lenfinder(coords[-1]) == lenfinder(coords[0]):
    return "equal", 0
  else:
    return "threep", lenfinder(coords[-1])

def internallen(crds):
  sizes = []
  for i in range(1, len(crds)-1):
    sizes.append(lenfinder(crds[i]))

  return max(sizes)

def lenfinder(coord):
  beg, end = coordfinder(coord)
  return end - beg + 1

def rlenfinder(coords):
  totrl = 0

  for coord in coords:
    totrl += lenfinder(coord)

  return totrl

file = sys.argv[1]

# The file has a few fields, but realy what needs to happen is to store the information in an efficient way. two dicts? hash

gtnames = []
chroms = []
strands = []
gt_coords = []
exp_name = []
exp_chroms = []
exp_coords = []
exp_strands = []
cases = []
detected = []
correct = []
o_typs = []
o_lens = []
iesizes = []
warns = []
covs = []
e_typs = []
# msa_fams = {}

rlen = None
with files.getfp(file) as fp:
  for line in fp:
    # has_MSA = False
    warn_needed = False
    iesize = "N/A"

    gtline, expline = line.rstrip().split()


    gt = gtline.split('|')

    chrom, gtname, _, gtcrd, strand = gtline.split('|')

    gtcrds = gtcrd.split(',')
    strand = strand[-1]

    if rlen == None:
      rlen = rlenfinder(gtcrds)
    # warning checks

    # MSA
    if '~' in expline:
      warn_needed = True
      has_MSA = True

    msa_fam = []
    case = casefinder(gtcrds, rlen)

    o_typ, o_len = gapfinder(gtcrds)

    if case == "internal":
      iesize = internallen(gtcrds)


    explines = expline.split("~")
    for expl in explines:
      if expl != "None":
        if expl.endswith('|'): expl = expl[0:-1]
        echrom, ename, estrand, ecrd = expl.split('|')
        ecrds = ecrd.split(',')
        detected.append("True")

      else:
        echrom, ename, estrand, ecrd = "None", "None", "None", "None"
        detected.append("False")
      
      cases.append(case)
      chroms.append(chrom)
      strands.append(strand)
      iesizes.append(iesize)

      exp_chroms.append(echrom)
      exp_coords.append(";".join(ecrds))
      exp_name.append(ename)
      exp_strands.append(estrand)

      gtnames.append(gtname)
      gt_coords.append(';'.join(gtcrds))

      o_typs.append(o_typ)
      o_lens.append(o_len)

      etyp, cov = accfinder(gtcrds, ecrds, case)

      covs.append(cov)
      e_typs.append(etyp)

      if not warn_needed:
        warns.append("-")
        continue

      elif has_MSA:
        warns.append("has_MSA")


 
# Stupid. Length checks.
assert(len(gtnames) == len(exp_name))
assert(len(gtnames) == len(strands))
assert(len(gtnames) == len(exp_strands))
assert(len(gtnames) == len(chroms))
assert(len(gtnames) == len(exp_chroms))
assert(len(gtnames) == len(gt_coords))
assert(len(gtnames) == len(exp_coords))
assert(len(gtnames) == len(warns))

#print(gtname, chrom, strand, gtcrds, isize, case, ename, echrom, estrand, ecrds, o_typ, o_len, cov)

# Output

print("gt_read", "gt_chrom", "gt_strand", "gt_coords", "ie_size", "case", "ex_read", "ex_chrom", "ex_strand", "ex_coords", "oh_type", "oh_len", "coverage", "err_typ", sep=',')


for i in range(len(gtnames)):
  print(gtnames[i], chroms[i], strands[i], gt_coords[i], iesizes[i], cases[i], exp_name[i], exp_chroms[i], exp_strands[i],  exp_coords[i], o_typs[i], o_lens[i], covs[i], e_typs[i], sep=',')