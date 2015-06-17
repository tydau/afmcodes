#!/usr/bin/python
#title			:hertz_calc.py
#description	:Calculator for Hertz model
#author			:T. Tyler Daugherty
#date			:20150616
#version		:0.1
#usage			:python hertz_calc.py
#notes			:
#python_version	:2.7.10
#Copyright 2015 T. Tyler Daugherty. All rights reserved.
#==============================================================================
from __future__ import division

hertz_force = lambda h, R, E, v: ((E * 10**(-12)) * 4 * (R**(0.5))*(h**(1.5)))/(3 * (1 - v**2))

def main():
    E_cell = 500
    r_afm = 2.5 #um
    v_cell = 0.49
    indent = float(raw_input('Indent (um):\n'))
    hf = hertz_force(indent, r_afm, E_cell, v_cell)
    print('Hertz prediction is '+ str(hf) +' N')

main()
