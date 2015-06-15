#!/usr/bin/python
#title			:para_gen.py
#description	:Generates paramter value list for COMSOL Cell Mechanics Cell Indent experiment.
#author			:T. Tyler Daugherty
#date			:20150611
#version		:01
#usage			:python para_gen.py
#notes			:
#python_version	:2.6.6
#==============================================================================

import sys
import numpy as np

start = float(raw_input("Starting point:\n"))
end = float(raw_input("Ending point:\n"))
int = float(raw_input("Inverval:\n"))
name_fwd = '/Users/tydau/GoogleDrive/research/afm/data/indents/cellindent_fwd.txt'
name_rev = '/Users/tydau/GoogleDrive/research/afm/data/indents/cellindent_rev.txt'

para_vals = list(np.arange(start,end+int,int))
parra_vals_rev = list(reversed(np.arange(start,end+int,int)))
para_vals = str(para_vals).strip('[]')
parra_vals_rev = str(parra_vals_rev).strip('[]')

file_fwd = open(name_fwd,'w')
file_rev = open(name_rev,'w')
file_fwd.write(para_vals)
file_rev.write(parra_vals_rev)
file_fwd.close()
file_rev.close()
