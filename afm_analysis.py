#!/usr/bin/python
#title			:afm_analysis.py
#description	:Script for analysis of data output by COMSOL simulation as .csv file
#author			:T. Tyler Daugherty
#date			:20150614
#version		:0.2
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
    return ([p0,p1])

def plotdata(data_plot,para_plot):
    #data, best fit vs. displacement as data_bestfit
    data_bestfit = figure(1)
    plot(data_plot[0],(data_plot[1]),'ro')
    plot(data_plot[0],(power_func(data_plot[0],para_plot[0],para_plot[1])))
    title('Force Curve of Cell Indentation')
    xlabel('Indentation of cell (um)')
    ylabel('Force (N)')

    data_hertzv = figure(2)
    plot(data_plot[0],data_plot[1],'bs')
    plot(data_plot[0],data_plot[2],'g^')

    show()

def main():
    #defines date,E_cell,v_cell, r_afm, and hertz_force as global variables
    global date, E_cell, v_cell, r_afm, hertz_force
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
    with open('/Users/tydau/GoogleDrive/research/afm/data/'+date+'/fc_rev_'+date+'.csv','rb') as csvrev:
        reader_rev = csv.reader(csvrev)
        fc_rev = list(reader_rev)

    with open('/Users/tydau/GoogleDrive/research/afm/data/'+date+'/fc_fwd_'+date+'.csv','rb') as csvfwd:
        reader_fwd = csv.reader(csvfwd)
        fc_fwd = list(reader_fwd)
    #delete first five terms from read-ins because this is useless for analysis
    del fc_fwd[0:5]
    del fc_rev[0:5]

    #reformat data such that data_* is an array with ([indention, force])
    data_fwd = reformat_data(fc_fwd)
    data_rev = reformat_data(fc_rev)

    #normalize indentation to Hertz convention
    data_fwd[0] = normalize_disp(data_fwd[0])
    data_rev[0] = normalize_disp(data_rev[0])

    #Find hertz predictions for data and store in data_*[2]
    hertz_fwd = data_fwd[0]
    hertz_rev = data_rev[0]
    hertz_fwd = [hertz_force(l, r_afm, E_cell, v_cell) for l in hertz_fwd]
    hertz_rev = [hertz_force(m, r_afm, E_cell, v_cell) for m in hertz_rev]
    data_fwd.append(hertz_fwd)
    data_rev.append(hertz_rev)

    #defines residues as data_*[3]
    data_fwd.append(getres(data_fwd))
    data_rev.append(getres(data_rev))

    #finds sum of squared residues
    fres_fwd = sum(data_fwd[3]**2)
    fres_rev = sum(data_rev[3]**2)

    para_fwd = getfit(data_fwd)
    para_rev = getfit(data_rev)

    plotdata(data_fwd,para_fwd)


main()
