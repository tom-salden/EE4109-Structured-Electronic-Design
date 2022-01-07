# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 20:43:11 2021

@author: tomsa
"""

from SLiCAP import *
import globalVariables
#prj = initProject('Active Antenna Design - Design group 3')

######## Input stage part ########
makeNetlist('SliCAP_Circuit.asc', 'Assignment 5 - Circuit analysis')
i2 = instruction()
i2.setCircuit('SliCAP_Circuit.cir')

i2.defPar('IG',0)
i2.defPar('L_A', globalVariables.L_A)
i2.defPar('C_A', globalVariables.C_A)
i2.defPar('C_F', globalVariables.C_F)

i2.defPar('W_DP', '800u')
i2.defPar('L_DP', '300n')
i2.defPar('ID_DP', '3.6m')

i2.defPar('W_P', '350u')
i2.defPar('W_N', '100u')

i2.defPar('L_N', '180n')
i2.defPar('L_P', '180n')


i2.defPar('ID_N', '300m')
i2.defPar('ID_P', '-300m')
i2.defPar('R1', 50)
i2.defPar('R2', 50)

head2html('Two-stage circuit analysis')

img2html('Assigment5_dual_stage_frequency.svg', 800)

text2html('Now the input stage is designed (in <a href="Assignment-5---Input-stage-design_index.html">Assignment 5 - Input stage design</a>) and the ouptut stage is designed (in <a href="Assignment-4---Complementary-parallel-CS-output-stage_index.html">Assignment 4 - Complementary-parallel CS output stage</a>), the total circuit can be characterised. In the image above, the total circuit can be seen. The parameters for the input transistors can be summarised with:')

eqn2html('W_DP',globalVariables.W_input*1e6, 'um')
eqn2html('L_DP',globalVariables.L_input*1e9, 'nm')
eqn2html('ID_DP',globalVariables.ID_input*1e3, 'mA')
eqn2html('W_N', globalVariables.Wn_output*1e6, 'um')
eqn2html('W_P', globalVariables.Wp_output*1e6, 'um')
eqn2html('L_N', globalVariables.Ln_output*1e9, 'nm')
eqn2html('L_P', globalVariables.Lp_output*1e9, 'nm')
eqn2html('ID_N', globalVariables.ID_n*1e3, 'mA')
eqn2html('ID_N', globalVariables.ID_p*1e3, 'mA')

text2html('The full circuit parameters can be found in the following section:')

htmlPage('Circuit parameters')
elementData2html(i2.circuit)
params2html(i2.circuit)

i2.setSimType('numeric')
i2.setSource('V1')
i2.setDetector('V_out')
i2.setLGref('Gm_M1_XU1')

i2.setGainType('loopgain')
i2.setDataType('pz')
pzResult = i2.execute()
polesLoopGain = pzResult.poles


htmlPage('Bandwidth and ploles and zeros of this solution')
text2html('After applying the values for this circuit, the bandwidth should be determined. If this bandwith is large enough, the amplifier can be used in this specific application. If it is too large, some bandwidth limitation techniques might have to be applied. The value of the bandwidth is as follows:')

i2.setDataType('laplace')
loopgain = i2.execute()
servoData = findServoBandwidth(loopgain.laplace)
Bf = servoData['lpf']
print('Bf: {0:1.2e}'.format(float(Bf)))
eqn2html('B_f',Bf*1e-9,'GHz')

text2html('In addition to the frequency derivation, the poles and zeros can be determined. They are displayed below:')

i2.setSimType('numeric')
i2.setSource('V1')
i2.setDetector('V_out')
i2.setLGref('Gm_M1_XU1')

i2.setGainType('gain')
i2.setDataType('pz')
pz2html(i2.execute())
i2.setDataType('laplace')
gain = i2.execute()

i2.setGainType('loopgain')
i2.setDataType('pz')
pz2html(i2.execute())
i2.setDataType('laplace')
loopgain = i2.execute()

i2.setGainType('asymptotic')
asymptotic = i2.execute()

i2.setGainType('servo')
servo = i2.execute()

i2.setGainType('direct')
direct = i2.execute()

htmlPage('Bode plots')
head2html('Bode plots')
text2html('Visible in the following bode plots is the frequency behaviour. The plot shows that the frequency behaviour of the amplifier is indeed flat until a frequency around $300 MHz$ is reached. This is still in line with the requirements.')
result = [asymptotic, gain, loopgain, servo, direct]
figdBmag = plotSweep('dBmag', 'dB magnitude', result, 10, 10e4, 100, sweepScale='M', funcType = 'dBmag', show=True)
figPhase = plotSweep('phase', 'Phase', result, 10, 10e4, 100, sweepScale='M', funcType = 'phase', show=True)
fig2html(figdBmag, 800)
fig2html(figPhase, 800)
