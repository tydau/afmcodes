#!/usr/bin/python
#title			:lameconversion.py
#description	:Converts E and v to Lame parameters
#author			:T. Tyler Daugherty
#date			:20150615
#version		:0.1
#usage			:python lameconversion.py
#notes			:
#python_version	:2.7.10
#Copyright 2015 T. Tyler Daugherty. All rights reserved.
#==============================================================================
from __future__ import division

def main():
    E = 500
    v = 0.49
    lame_lambda = (v*E)/((1+v)*(1-2*v))
    lame_mu = E/(2*(1+v))
    print lame_lambda, lame_mu

main()
