# -*- coding: utf-8 -*-
"""
Created on Fri Jan  7 17:11:58 2022

@author: tomsa
"""

from SLiCAP import *
import globalVariables
from pythonfunctions import *

makeNetlist('Assignment6-frequencyCompensation-rlphz.asc', 'Assignment 6 - Biasing')
i1 = instruction()
i1.setCircuit('Assignment6-frequencyCompensation-rlphz.cir')

i1.defPar('IG',0)
i1.defPar('L_A', globalVariables.L_A)
i1.defPar('C_A', globalVariables.C_A)
i1.defPar('C_F', globalVariables.C_F)

i1.defPar('W_DP', '800u')
i1.defPar('L_DP', '300n')
i1.defPar('ID_DP', '3.6m')

i1.defPar('W_P', '350u')
i1.defPar('W_N', '100u')

i1.defPar('L_N', '180n')
i1.defPar('L_P', '180n')


i1.defPar('ID_N', '1.14m')
i1.defPar('ID_P', '-1.14m')
i1.defPar('R1', 50)
i1.defPar('R2', 50)

R_phz = 13.81
L_phz = 4e-7

i1.defPar('Rphz',R_phz)         #Input Phantom Zero
i1.defPar('Lphz',L_phz)         #Output Phantom Zero

i1.setSimType('numeric');
i1.setGainType('gain');
i1.setDataType('laplace');
i1.setSource('V1');
i1.setDetector('V_out');
gainEKV = i1.execute()

htmlPage('Biasing of the circuit with current sources and floating sources')

text2html('After determining the circuit performances in SLiCAP, a real implementation of the circuit has to be fabricated that can be simulated in programs like LTSpice. Correct biasing of the transistors is crucial for this step to ensure that the devices are in their correct operating regions. Some decisions have been made on how to bias the circuit:')

text2html('The common-mode voltage of the amplifier is $900 mV$. Therefore, the input and output of each state should read $900 mV$ with 0 signal input.')

head2html('Biasing of the input stage')
text2html('Like determined, the common mode voltage of the amplifier should be $900 mV$. Therefore, voltage at the input and output can be set at this level. In addition, the drain current through the transistors should be $3.6 mA$, therefore a sinking current source can be added that sinks 2x the drain current ($7.2 mA$).')
img2html('A6-InputBiasing-step1.svg',600)

text2html('To complete the biasing, some logical deducions can be made. Since there should not be any output signal when there is no input signal, the gate voltage of M2 should equal the gate voltage of M1. In addition, the drain voltage of M1 should equal the drain voltage of M2. These voltages can be created by using voltage sources. Finally, the current needs to be divided equally between the two transistors. To force this division, a current souce at the output can be placed. This can be done because the input of the next stage has a high input impedance. The following image shows the biased input stage.')
img2html('A6-InputBiasing-step2.svg',600)

head2html('Biasing of the ouput stage')
text2html('The biased output circuit has already been used in this project in <a href="Assignment-4---Complementary-parallel-CS-output-stage_index.html">Assignment 4 - Complementary-parallel CS output stage</a>. The biased circuit was used to determine the operating points of the transistors, therefore this design can be used in the biased circuit as well.')
img2html('A6-OutputBiasing.svg',600)

head2html('Biasing of the full circuit')
text2html('The full circuit can now be implemented by using the biased input and output stages. One additional component is necessary, a resistor in the feedback loop. This resistor passes DC signal and feeds back the $900 mV$ from the output to the input of the amplifier, making sure that the common mode voltage is the same along the entire amplifier. In addition, to get rid of the common-mode voltage, a capacitor is placed in series before the output.')
img2html('BiasingStep1.svg',800)

head2html('Small signal dynamic response')
LTmag_out, LTphase_out = LTspiceAC2SLiCAPtraces('BiasingStep1-ac.txt')

mag_bias1 = plotSweep('mag_bias1', 'magnitude of the biased amplifier', gainEKV, 1e3, 10e9, 200, funcType = 'mag', show=True)
traces2fig(LTmag_out, mag_bias1)
mag_bias1.plot()
fig2html(mag_bias1, 800)

phase_bias1 = plotSweep('phase_bias1', 'phase of the biased amplifieer', gainEKV, 1e3, 10e9, 200, funcType = 'phase', show=True)
traces2fig(LTphase_out, phase_bias1)
phase_bias1.plot()
fig2html(phase_bias1, 800)


head2html('Noise behaviour')
LTnoise, empty = LTspiceDC2SLiCAPtraces('BiasingStep1-noise.txt')

figLT_noise = plot('LTnoise_bias1', 'Noise simulation of the biased amplifier', 
                'semilogx', LTnoise, xName='frequency', xUnits='Hz',
                yName='$Input referred noise$', yUnits = '$V/Hz^{1/2}$', show=True)
fig2html(figLT_noise, 800)

head2html('Drive capability')


head2html('Weak nonlinearity')


htmlPage('Biasing of the circuit with implementation of floating sources')

head2html('Implementation of floating sources')

head2html('Conclusion on amplifier performance')

htmlPage('Biasing of the circuit with implementation of current sources')

head2html('Implementation of currents sources')

head2html('Conclusion on amplifier performance')

htmlPage('LTspice results')


htmlPage('Comparision LTspice and SLiCAP')
head2html('Small signal dynamic response')
head2html('Noise behaviour')
head2html('Drive capability')
head2html('Weak nonlinearity')