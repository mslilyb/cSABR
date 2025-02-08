import os
import platform
import src.constants as bconsts
import warnings

"""
Validation tools and error handling for bakeoff scripts.
"""

def watchbake():
	return None

def verifyprograms(progs):
	for prog in progs:
		if prog not in bconsts.BAKEPROGS:
			raise NameError(f'Program {prog} not found in bakeoff programs (did you mispell anything?)')
