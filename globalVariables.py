# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 17:25:55 2021

@author: tomsa
"""
#Define global parameters used throughout the desing

L_A = 0.5           #Antenna length
C_A = 10e-12        #Antenna capacitance
C_F = L_A*C_A

S_floor = 6.25e-18  #Noise floor at higher frequencies

#Empty variables, filled in by scripts itself
W_input = 400*10**(-6) * 2    #Width of the transistors of the DIFFERENTIAL PAIR
L_input = 300*10**(-9)        #Length of the transistors of the DIFFERENTIAL PAIR
ID_input = 1.8*10**(-3) * 2   #Drain current of the DIFFERENTIAL PAIR

Wn_output = 100e-6       #Width of the push-pull stage NMOS
Ln_output = 180e-9       #Length of the push-pull stage NMOS
Wp_output= 350e-6        #Width of the push-pull stage PMOS
Lp_output = 180e-9       #Length fo the push-pull stage PMOS
ID_n = 300e-3            #Drain current of NMOS
ID_p = 300e-3            #Drain current of PMOS