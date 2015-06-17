#!/usr/bin/python
#title			:analysis_afm.py
#description	:Analysis software for AFM FEM Simulation
#author			:T. Tyler Daugherty
#date			:20150617
#version		:0.1
#usage			:python analysis_afm.py
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


def reformat_data(listfile):
    #define empty lists para, forces, and disp for para, forces, and displacement parameters
    forces_list = []
    disp_list = []
    #add values to previously defined lists as float values
    for i, j in enumerate(listfile):
        forces_list.append(float(listfile[i][1]))
        disp_list.append(float(listfile[i][2]))
    data_array = ([np.array(disp_list),np.array(forces_list)])
    #outputs data in proper array with format as float
    return data_array

def normalize_disp(disp):
    return [-n for n in disp]

def getres(datas):
    return datas[1] - datas[2]

def getfit(data_getfit):
    #defines function for fit
    global power_func
    power_func = lambda x, a, b: a * (x**b)
    popt, pcov = curve_fit(power_func, data_getfit[0], data_getfit[1])
    #define p0 as a best fit parameter for data with func
    p0 = popt[0]
    #define p1 as b best fit parameter for data with func
    p1 = popt[1]
    print('p0 = '+str(p0))
    print('p1 = '+ str(p1))
    return ([p0,p1])

def plotdata(data_plot,para_plot):
    p0_plot = str(para_plot[0])
    p1_plot = str(round(para_plot[1],2))
    p2_plot = str(para_plot[2])

    #data, best fit vs. displacement as data_bestfit
    plot(data_plot[0],1e12*(data_plot[1]),'ro')
    plot(data_plot[0],1e12*(power_func(data_plot[0],para_plot[0],para_plot[1])))
    legend()
    title('Force Curve of Cell Indentation')
    xlabel('Indentation of cell (um)')
    ylabel('Force (pN)')
    text(0.1,2000000,'Fit equation: F = K*(h**b) | b='+p0_plot+', K='+p1_plot)
    text(0.1,1900000,'Sum of residues squared to Hertz model:' + p2_plot)

    show()

def main():
    #defines date,E_cell,v_cell, r_afm, and hertz_force as global variables
    global date, E_cell, v_cell, r_afm, hertz_force
    #filename for file in '/Users/tydau/GoogleDrive/research/afm/data/'+date+'/fc_fwd_'
    file = raw_input('Input filename with extention.csv:\n')
    #date of data for proper file location
    date = '06.12.2015'
    #Young's modulus of cell in Pa
    E_cell = 500 #Pa
    #Poisson ratio of cell
    v_cell = 0.49
    #Radius of AFM tip in um
    r_afm = 2.5
    #Hertz model
    hertz_force = lambda h, R, E, v: ((E * 10**(-12)) * 4 * (R**(0.5))*(h**(1.5)))/(3 * (1 - v**2))
    #read csv files
    with open('/Users/tydau/GoogleDrive/research/afm/data/'+date+'/'+file,'rb') as csv_raw:
        reader_raw = csv.reader(csv_raw)
        raw_data = list(reader_raw)
    #delete first five terms from read-ins because this is useless for analysis
    del raw_data[0:5]

    #reformat data such that data_* is an array with ([indention, force])
    data = reformat_data(raw_data)

    #normalize indentation to Hertz convention
    data[0] = normalize_disp(data[0])

    #Find hertz predictions for data and store in data_*[2]
    hertz_data = data[0]
    hertz_data = [hertz_force(l, r_afm, E_cell, v_cell) for l in hertz_data]
    data.append(hertz_data)

    #defines residues as data_*[3]
    data.append(getres(data))

    #finds sum of squared residues
    fres = sum(data[3]**2)

    print('Forward Data Analysis\n')
    para = getfit(data)
    para.append(fres)
    print('Residual sum of squares: '+str(fres))

    plotdata(data,para)


main()
