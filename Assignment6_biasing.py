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
img2html('BiasingStep1.svg',1000)

text2html('The next step is to find out if the circuit actually behaves like expected and to see where the behaviour differs from the SLiCAP simulation. The following figures display the performance of this first step of the biased amplifier.')

head2html('Small signal dynamic response')
text2html('The following graphs display the bode plots of the SLiCAP simulation with the LTSpice simulation on top. Both traces are very similar and only at high frequencies, the simulations differ a little bit. At low frequencies, the LTSpice phase deviates a bit from the 180 degrees, unlike the SLiCAP simulation. The reason is that a capacitor is added at the output of the amplifier, causing an extra pole at low frequencies. If the value of the capacitor is decreased, this effect is enlarged and a drop in gain is visible as well.')
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
text2html('The noise behaviour of the amplifier is more than adequate. At $10 kHz$, the noise requirement is $100 nV/mHz^{1/2}$. In this case, it is $22.5 nV/mHz^{1/2}$. At $100 kHz$, the requirements are $10 nV/mHz^{1/2}$. The amplifier is at $5 nV/mHz^{1/2}$. In addition, the requirement for noise floor of $5 nV/mHz^{1/2}$ is also met. This means that there is still some room left for the rest of the biasing steps.')
LTnoise, empty = LTspiceDC2SLiCAPtraces('BiasingStep1-noise.txt')

figLT_noise = plot('LTnoise_bias1', 'Noise simulation of the biased amplifier', 
                'semilogx', LTnoise, xName='frequency', xUnits='Hz',
                yName='$Input referred noise$', yUnits = '$V/mHz^{1/2}$', show=True)
fig2html(figLT_noise, 800)

head2html('Drive capability')
text2html('The amplifier should be able to drive at least $316 mV$. By applying an input voltage that is too high, the maximum drive capability can be identified at the output. From this figure, it is clear that the amplifier is able to drive around $400 mV$, which is enough.')
LTdrive, empty = LTspiceDC2SLiCAPtraces('BiasingStep1-driveCapabilities.txt')

figLT_drive = plot('LTdrive_bias1', 'Transient simulation of the biased amplifier', 
                'lin', LTdrive, xName='time', xUnits='s',
                yName='$Output voltage$', yUnits = '$V$', show=True)
fig2html(figLT_drive, 800)


head2html('Weak nonlinearity')
text2html('The weak nonlinearity is tested by applying 2 input signals, one at $10 MHz$ and one at $12 MHz$. The amplitude of both of the signals are half of the maximum input amplitude. The simulation is ran for $1600 ns$ and the maximum timestep is $1 ns$. The peaks of these signals have an amplitude of $-25 dB$, while the steady portion of the figure has an amplitude of $-76 dB$, which is slightly bigger than the necessary $50 dB$.')
LTimd, empty = LTspiceAC2SLiCAPtraces('BiasingStep1-imd.txt', True)

figLT_imd = plot('LTimd_bias1', 'Intermodular distortion of the biased amplifier', 
                'semilogx', LTimd, xName='frequency', xUnits='Hz',
                yName='$Signal strength$', yUnits = '$dB$', show=True)
fig2html(figLT_imd, 800)

htmlPage('Biasing of the circuit with implementation of floating sources')

head2html('Implementation of floating sources')
text2html('The next step of biasing is to swap out the floating voltage sources for transistor implementations. The following figure shows the chosen implementation to create floating sources.')

img2html('BiasingFloatingSource.svg',800)

head2html('Biased circuit')
text2html('After implementation, the full circuit is shown in the following figure. One other change is that the voltage on the source of the first transistor of the differential pair is adjusted for the lower common-mode voltage after the differential pair. This has no drastic influences on the performance of the amplifier')

img2html('BiasingStep2.svg',1000)

head2html('Conclusion on amplifier performance')
text2html('The performance of the amplifier is still within specs after creating the floating sources. The AC analysis barely changes, the noise performance has enough headroom for the added transistors and resistors and the amplifier can still drive around $400 mV$. There is a little more weak nonlinearity, but it still is within specifications as seen in the following figure.')

LTimd, empty = LTspiceAC2SLiCAPtraces('BiasingStep2-imd.txt', True)

figLT_imd = plot('LTimd_bias2', 'Intermodular distortion of the biased amplifier', 
                'semilogx', LTimd, xName='frequency', xUnits='Hz',
                yName='$Signal strength$', yUnits = '$dB$', show=True)
fig2html(figLT_imd, 800)

htmlPage('Biasing of the circuit with implementation of current sources')
head2html('Implementation of currents sources')
text2html('A current source is traditionally made with a current mirror. The same is used for this amplifier circuit. The following current mirror is used for the two current sources that are necessary. In the ciruit there are two kinds of current sources used. One source supplies current to one of the branches of the differential pair and the other current source sinks current. Therefore, two different current sources need to be designed. One current source that sources $3.6mA$ to the differential pair and one that sinks $7.2mA$ from the stage to ground. The following figure shows the implementation of the two sources.')

img2html('BiasingCurrentSource.svg', 800)

head2html('Full circuit')
img2html('BiasingStep3.svg', 1000)
text2html('The circuit in this figure is the biased amplifier with the implemented current sources. Some fine-tuning was necessary for the sources to fit in the circuit, so the sizing has been adjusted in comparison to the figure above. In addition, some resistors are omitted due to the noise floor limit. The current sources add a relatively big amount of input-referred noise, therefore careful tuning was necessary to stick to the limit. The performance of this circuit will be discussed in the next section')

htmlPage('Final biased circuit')

head2html('Final structured circuit')
img2html('BiasingStep4.svg', 1000)

text2html('Now all floating voltage sources and current sources are replaced by transistor implementations, the circuit is fully biased to the point that it can be powered with several voltage sources. The figure shown here is the restructured schematic of the biased circuit displayed in the previous section.')

text2html('Finally, the circuit is tested with the same simulations as the unbiased circuit. This is done to make sure the biasing did not introduce unwanted effects.')

head2html('Small signal dynamic response')
text2html('The AC-analysis of the circuit is not changed visibly from the circuit biased with ideal sources, therefore the circuit still behaves as is expected.')
LTmag_out, LTphase_out = LTspiceAC2SLiCAPtraces('BiasingStep3-ac.txt')
figLT_mag = plot('mag_bias3', 'Magnitude of the biased amplifier', 
                'log', LTmag_out, xName='frequency', xUnits='Hz',
                yName='Magnitude', yUnits = '', show=True)
figLT_phase = plot('phase_bias3', 'Phase of the biased amplifier', 
                'semilogx', LTphase_out, xName='frequency', xUnits='Hz',
                yName='Phase', yUnits = 'deg', show=True)


fig2html(figLT_mag, 800)
fig2html(figLT_phase, 800)

head2html('Noise behaviour')
text2html('Like mentioned in the previous section, the implementation of the current sources introduced a relatively big amount of noise. However, the final circuit still abides to the requirements. The most critical point is at $1 MHz$, where the noise is required to be $5 nV/mHz^{1/2}$. The final value is just below this requirement. One method of decreasing this noise is to resize the input stage. If the length and drain current are decreased, the noise floor drops. However, it is not necessary for this design.')
LTnoise, empty = LTspiceDC2SLiCAPtraces('BiasingStep3-noise.txt')

figLT_noise = plot('LTnoise_bias3', 'Noise simulation of the biased amplifier', 
                'semilogx', LTnoise, xName='frequency', xUnits='Hz',
                yName='$Input referred noise$', yUnits = '$V/mHz^{1/2}$', show=True)
fig2html(figLT_noise, 800)

head2html('Drive capability')
text2html('Similarly to the circuit biased wit ideal sources, this circuit is able to drive the load up to about $400mV$, which is sufficient for the requirements.')
LTdrive, empty = LTspiceDC2SLiCAPtraces('BiasingStep3-driveCapabilities.txt')

figLT_drive = plot('LTdrive_bias3', 'Transient simulation of the biased amplifier', 
                'lin', LTdrive, xName='time', xUnits='s',
                yName='$Output voltage$', yUnits = '$V$', show=True)
fig2html(figLT_drive, 800)

head2html('Weak nonlinearity')
text2html('Finally, the weak nonlinearity did not change significantly since adding the floating voltage sources. This means that the requirements are still met for this part.')
LTimd, empty = LTspiceAC2SLiCAPtraces('BiasingStep3-imd.txt', True)

figLT_imd = plot('LTimd_bias3', 'Intermodular distortion of the biased amplifier', 
                'semilogx', LTimd, xName='frequency', xUnits='Hz',
                yName='$Signal strength$', yUnits = '$dB$', show=True)
fig2html(figLT_imd, 800)

