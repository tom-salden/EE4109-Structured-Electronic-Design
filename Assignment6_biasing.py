# -*- coding: utf-8 -*-
"""
Created on Fri Jan  7 17:11:58 2022

@author: tomsa
"""

makeNetlist('emptyCircuit.asc', 'Assignment 6 - Biasing')
i1 = instruction()
i1.setCircuit('emptyCircuit.cir')

htmlPage('Biasing of the circuit')

head2html('Biasing of the ouput stage')

head2html('Biasing of the input stage')

htmlPage('LTspice results')


htmlPage('Comparision LTspice and SLiCAP')