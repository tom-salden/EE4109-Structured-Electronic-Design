
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 20:21:00 2021

@author: anton
"""

from SLiCAP import *
from pythonfunctions import *

makeNetlist('CSstageEKV.asc', 'Assignment 2 - Modelling the transistor');
i1 = instruction();
i1.setCircuit('CSstageEKV.cir')


# Convert LTspice AC analysis output to SLiCAP traces
LTmag_out, LTphase_out = LTspiceAC2SLiCAPtraces('LTspiceCSstage-transimpedance.txt')
LTmag_inp, LTphase_inp = LTspiceAC2SLiCAPtraces('LTspiceCSstage-InputImpedance.txt')

htmlPage('LTspice circuit transfer')
head2html('LTspice operating point and AC analysis')
img2html('LTspiceCSstage.svg', 800)


head2html('Transimpedance')

figLTmag_out = plot('LTmag-out', 'AC simulation magnitude charactersitics of the transimpedance', 
                'log', LTmag_out, xName='frequency', xUnits='Hz',
                yName='$V_{out}$', yUnits = '$\\Omega$', show=True)

figLTphase_out = plot('LTphase-out', 'AC simulation phase charactersitics of the transimpedance', 
                'semilogx', LTphase_out, xName='frequency', xUnits='Hz',
                yName='$arg(V_{out})$', yUnits = 'deg', show=True)

# Place the plots on the HTML active page
fig2html(figLTmag_out, 600, caption='LTspice AC analysis magnitude of $Z_t$.')
fig2html(figLTphase_out, 600, caption='LTspice AC analysis phase of $Z_t$.')

head2html('Input impedance')

figLTmag_inp = plot('LTmag-inp', 'AC simulation magnitude charactersitics of the input impedance', 
                'log', LTmag_inp, xName='frequency', xUnits='Hz',
                yName='$V_{out}$', yUnits = '$\\Omega$', show=True)

figLTphase_inp = plot('LTphase-inp', 'AC simulation phase charactersitics of the input impedance', 
                'semilogx', LTphase_inp, xName='frequency', xUnits='Hz',
                yName='$arg(V_{out})$', yUnits = 'deg', show=True)

# Place the plots on the HTML active page
fig2html(figLTmag_inp, 600, caption='LTspice AC analysis magnitude of $Z_t$.')
fig2html(figLTphase_inp, 600, caption='LTspice AC analysis phase of $Z_t$.')






htmlPage('SLiCAP approximation, comparison, symbolic transfer and numeric values')
#from CSstageLTspice import LTmag, LTphase

# Uncomment the next line if you want to overwrite the main html index page
#prj = initProject('CSstageSmallSignal');

# Generate netlist

# This creates an new index page in the html report and links to new pages
# will now be placed on this index page


# Obtain the values of the small-signal parameters according to the EKV model,
# the C18 process parameters and the device geometry. They are calculated
# using the model equations in the subcircuit X1: CMOS18N
# We will pass these values to other circuits.
# 
# You could also obtain these values from a lookup table and correct them for 
# the device geometry and operating conditions

gm = i1.getParValue('g_m_XU1')
go = i1.getParValue('g_o_XU1')
cgs = i1.getParValue('c_gs_XU1')
cgb = i1.getParValue('c_gb_XU1')
cdg = i1.getParValue('c_dg_XU1')
cdb = i1.getParValue('c_db_XU1')

i1.setSimType('numeric');
i1.setGainType('gain');
i1.setDataType('laplace');
i1.setSource('I1');
i1.setDetector('V_out');
gainEKV = i1.execute()

head2html('Transimpedance')
magZtEKV_out = plotSweep('magZtEKV_out', 'magnitude of the transimpedance', gainEKV, 1, 100e9, 200, funcType = 'mag', show=True)
traces2fig(LTmag_out, magZtEKV_out)
magZtEKV_out.plot()
fig2html(magZtEKV_out, 600)
phaseZtEKV_out = plotSweep('phaseZtEKV_out', 'phase of the transimpedance', gainEKV, 1, 100e9, 200, funcType = 'phase', show=True)
traces2fig(LTphase_out, phaseZtEKV_out)
phaseZtEKV_out.plot()
fig2html(phaseZtEKV_out, 600)


head2html('Input impedance')
i1.setSimType('numeric');
i1.setGainType('gain');
i1.setDataType('laplace');
i1.setSource('I1');
i1.setDetector('V_in');
gainEKV = i1.execute()

magZtEKV = plotSweep('magZtEKV', 'magnitude of the input impedance', gainEKV, 1, 100e9, 200, funcType = 'mag', show=True)
traces2fig(LTmag_inp, magZtEKV)
magZtEKV.plot()
fig2html(magZtEKV, 600)
phaseZtEKV = plotSweep('phaseZtEKV', 'phase of the input impedance', gainEKV, 1, 100e9, 200, funcType = 'phase', show=True)
traces2fig(LTphase_inp, phaseZtEKV)
phaseZtEKV.plot()
fig2html(phaseZtEKV, 600)


htmlPage('Symbolic transfer and numeric values')
i1.setSimType('symbolic');
i1.setGainType('gain');
i1.setDataType('laplace');
i1.setSource('I1');
i1.setDetector('V_out');
gainEKV = i1.execute()

head2html('Symbolic expression of transimpedance')
eqn2html('Z_t', gainEKV.laplace)

i1.setSimType('numeric');
i1.setDataType('pz')
pz2html(i1.execute())

i1.setSimType('symbolic');
i1.setGainType('gain');
i1.setDataType('laplace');
i1.setSource('I1');
i1.setDetector('V_in');
gainEKV = i1.execute()

head2html('Symbolic expression of input impedance')
eqn2html('Z_t', gainEKV.laplace)

i1.setSimType('numeric');
i1.setDataType('pz')
pz2html(i1.execute())