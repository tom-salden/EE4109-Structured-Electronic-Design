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
i1 = instruction()
i1.setCircuit('SliCAP_Circuit.cir')

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


i1.defPar('ID_N', '300m')
i1.defPar('ID_P', '300m')
i1.defPar('R1', 50)
i1.defPar('R2', 50)

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
elementData2html(i1.circuit)
params2html(i1.circuit)

i1.setSimType('numeric')
i1.setSource('V1')
i1.setDetector('V_out')
i1.setLGref('Gm_M1_XU1')

i1.setGainType('loopgain')
i1.setDataType('pz')
pzResult = i1.execute()
polesLoopGain = pzResult.poles


htmlPage('Bandwidth of this solution')
text2html('After applying the values for this circuit, the bandwidth should be determined. If this bandwith is large enough, the amplifier can be used in this specific application. If it is too large, some bandwidth limitation techniques might have to be applied. The value of the bandwidth is as follows:')

i1.setDataType('laplace')
loopgain = i1.execute()
servoData = findServoBandwidth(loopgain.laplace)
Bf = servoData['lpf']
print('Bf: {0:1.2e}'.format(float(Bf)))
eqn2html('B_f',Bf*1e-9,'GHz')


