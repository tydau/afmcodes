#!/usr/bin/python
#title			:afm_analysis.py
#description	:Script for analysis of data output by COMSOL simulation as .csv file
#author			:T. Tyler Daugherty
#date			:20150614
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

#read csv files
with open('/Users/tydau/GoogleDrive/research/afm/data/'+date+'/fc_rev_'+date+'.csv','rb') as csvrev:
    reader_rev = csv.reader(csvrev)
    fc_rev = list(reader_rev)

with open('/Users/tydau/GoogleDrive/research/afm/data/'+date+'/fc_fwd_'+date+'.csv','rb') as csvfwd:
    reader_fwd = csv.reader(csvfwd)
    fc_fwd = list(reader_fwd)

#delete first five terms from read-ins because this is useless for analysis
del fc_fwd[0:5]
del fc_rev[0:5]

#define function to reformat data which is currently in nested list format with output as array with floats
def reformat_lists(listfile):
    #define empty lists para, forces, and disp for para, forces, and displacement parameters
    para_list = []
    forces_list = []
    disp_list = []
    #add values to previously defined lists as float values
    for i, j in enumerate(listfile):
        para_list.append(float(listfile[i][0]))
        forces_list.append(float(listfile[i][1]))
        disp_list.append(float(listfile[i][2]))
    data_array = ([np.array(para_list),np.array(disp_list),np.array(forces_list)])
    #outputs data in proper array with format as float
    return data_array

#reformat lists to arrays with float values as per function
data_fwd = reformat_lists(fc_fwd)
data_rev = reformat_lists(fc_rev)
#take -1* values in displacement for convention of Hertz model
data_fwd[1] = [-n for n in data_fwd[1]]
data_rev[1] = [-n for n in data_rev[1]]
#concatonate data into one array set
#Format of data_* = ([para, displacement, force])

#Hertz force equation
hertz_force = lambda h, R, E, v: (E * 4 * (R**(0.5))*(h**(1.5)))/(3 * (1 - v**2))
hertz_th = data_fwd[2]
hertz_th = [hertz_force(i, r_afm, E_cell, v_cell) for i in hertz_th]
data_fwd.append(hertz_th)
#Power function for fit with data
power_func = lambda x, a, b: a * (x**b)

#curve-fit to func
popt, pcov = curve_fit(power_func, data_fwd[1], data_fwd[2])

#define p0 as a best fit parameter for data with func
p0 = popt[0]
#define p1 as b best fit parameter for data with func
p1 = popt[1]

#print parameters
print('p0 = '+ str(p0))
print('p1 = ' +  str(p1))

#find residuals of data
residuals = data_fwd[2] - hertz_th
#determines residual sum of squares, remember that a low fres will mean a high correlation to the model
fres = sum(residuals**2)

print('Sum of residuals squared = '+ str(fres))

##################
#Plotting data
##################

#data, best fit vs. displacement as data_bestfit
data_bestfit = figure(1)
plot(data_fwd[1],(data_fwd[2]),'ro')
plot(data_fwd[1],(power_func(data_fwd[1],p0,p1)))
title('Force Curve of Cell Indentation')
xlabel('Indentation of cell (um)')
ylabel('Force (mN)')


#data_log as plot of log10 of each measurement
data_log = figure(2)
plot(log10(data_fwd[1]), log10(1000*data_fwd[2]), 'bs')
title('Log10 Plot of Force Curve of Cell Indentation Data')
xlabel('log10(Cell Indentation) (log10(um))')
ylabel('log10(Resultant Force) (log10(mN))')

show()
