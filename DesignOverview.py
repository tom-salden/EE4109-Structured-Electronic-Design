# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 12:20:11 2021

@author: Design Group 3
"""
from SLiCAP import *

makeNetlist('emptyCircuit.asc', 'Design Overview')
i1 = instruction()
i1.setCircuit('emptyCircuit.cir')

head2html('Design requirements')
text2html('The design requirements for the active antenna')
