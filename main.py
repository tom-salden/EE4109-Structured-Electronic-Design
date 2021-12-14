# -*- coding: utf-8 -*-
"""
EE4109 - Structured Electronic Design
Design group 3

"""
#Clean up the html folder, so no extra files persist
import shutil
shutil.rmtree('html')

#Clean up variables and console to get a 'clean' run
try:
    from IPython import get_ipython
    get_ipython().magic('clear')
    get_ipython().magic('reset -f')
except:
    pass

#Create a project
from SLiCAP import *
prj = initProject('Active Antenna Design - Design group 3')

#Define global parameters used throughout the desing


#Run all assignments sequentially.
import DesignOverview
import Assignment1
import Assignment2
import Assignment3NoiseWithoutFlicker
import Assignment3NoiseWithFlicker
import Assignment4
import Assignment5