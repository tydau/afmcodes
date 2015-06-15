#!/usr/bin/python
#title			:afm_analysis.py
#description	:Analysis code for COMOSL .csv output
#author			:T. Tyler Daugherty
#date			:20150615
#version		:0.1
#usage			:python afm_analysis.py
#notes			:
#python_version	:2.7.10
#Copyright 2015 T. Tyler Daugherty. All rights reserved.
#==============================================================================

from __future__ import division
import csv
import numpy as np
from pylab import *
from scipy import *
from scipy.optimize import curve_fit

#date of data for proper file location
date = '06.12.2015'
#Young's modulus of cell in Pa
E_cell = 500 #then with 250 to see if big change
#Poisson ratio of cell
v_cell = 0.49
#Radius of AFM tip in um
r_afm = 2.5
