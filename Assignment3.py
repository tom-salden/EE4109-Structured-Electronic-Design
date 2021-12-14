from SLiCAP import *


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Noise analysis without flicker
"""
from SLiCAP import *

i1 = instruction()
i1.setCircuit('Assignment3_attempt2.cir')
# create an html page for the results
htmlPage('Noise analysis without flicker noise')
# Discard 1/f noise
KF_N18 = i1.getParValue('KF_N18')
W = i1.getParValue('W')
i1.defPar('KF_N18', 0)

text2html('The values are the same as that of the previous assignment')
img2html('Assignment3.png', 700)
# print important operating point parameters
text2html('The inversion coefficient $IC$ equals: ' +
          '%s'%(sp.N(i1.getParValue('IC_XU1'), ini.disp)))
text2html('The critical inversion coefficient $IC_{CRIT}$ equals: ' +
          '%s'%(sp.N(i1.getParValue('IC_CRIT_XU1'), ini.disp)))
text2html('The transconductance $g_m$ equals: ' +
          '%s'%(sp.N(i1.getParValue('g_m_XU1'), ini.disp)))
# calculate source referred noise spectrum
i1.setSource('V1')
i1.setDetector('V_out')
i1.setGainType('vi')
i1.setDataType('Noise')
i1.setSimType('numeric')
noiseResult = i1.execute()

c_iss = i1.getParValue('c_iss_XU1')
print(c_iss)

head2html('Source referred noise')
iNoise = sp.sqrt(noiseResult.inoise)
text2html('The spectrum of the source-referred voltage noise [V/rt(Hz)] ' +
          'is: %s'%(sp.N(iNoise, ini.disp)))
text2html('Here is the source refered noise.');
figSin = plotSweep('CScapNoiseVspectrum','Input noise spectrum', noiseResult,
                   10e3, 30e9, 100, funcType='inoise', show = True)
i1.defPar('KF_N18', KF_N18)
noiseResult = i1.execute()
fig_flicker = plotSweep('flicker_noise','Input noise spectrum', noiseResult,
                   10e3, 30e9, 100, funcType='inoise', show = True)
fig2html(figSin,  500)
i1.defPar('KF_N18', 0)
# Find the width for the lowest noise
text2html('But we want to know for which width we still have more noise than the minimum requirements.')
text2html('At the minimum, we need to have less noise than $2.5$ nVHz$^{-0.5}$ (See the antenna requirements)')
text2html('To calculate the minimum width, we plot the source refered input noise vs the width of the device. Note that the device is kept in critical inversion')


# Delete the numeric definition of W so we can calculate the optimum value 
# symbolically
i1.delPar('W')
# Keep IC at IC_CRIT
i1.defPar('ID', '7.44m*W/66u');
Svi_f_W = i1.execute().inoise


i1.defPar('Vni', sp.sqrt(Svi_f_W))
# Redefine the width so it can be used as sweep variable, any value is K


i1.defPar('W', 0)
i1.setDataType('params')
result = i1.execute()
fig_Vni_W = plotSweep('Vni_W', 'Source-referred noise voltage versus ' +
                      'width', 
                     result, 5, 20, 200, sweepVar = 'W', sweepScale = 'u', 
                     funcType = 'param', xUnits = 'm', yVar = 'Vni', 
                     yUnits = 'V / sqrt(Hz)', yScale='n', show = True)
fig2html(fig_Vni_W, 500)
text2html('From this we can read out that we have a showstopper. If $W < 7 \mu m$, the design will fail nonetheless. However, for wider widths the noise performance meets the requirements. ')
text2html('The optimum noise performance would be achieved if $C_s = c_{iss}$, which would result in a width of 2.5mm')
text2html('For our current W/L ratio, we obtain a $C_{iss}$ of $8.7 \cdot 10^{-14}$ F')
text2html('Although the width of 2.5mm is the optimum, such a large value is not needed for the noise requirements')


htmlPage('Flicker noise analysis')


text2html('In this analysis we will also take 1/f noise into account. The 1/f noise limit can be described using the equation:')
text2html('$S_{en}(f) \le S_{em,floor} ( 1 + \dfrac{f_c}{f^2} )$')
text2html('Where $S_{em,floor} = 2.5 \cdot 10^{-17} V^2/Hzm^2$ and with corner frequency $f_c = 200$ kHz')


text2html('We have a showstopper if the following condition is not met')
text2html('$8/3 KF < S_{em,floor} L_A^2f_cC_a$')
text2html('For our design, $KF = 3 \cdot 10^{-25}$, $L_A = 0.5m$, $f_c = 200 \cdot 10^3 Hz$, $S_{em,floor} = 2.5 \cdot 10^{-17}$ and $C_a = 5pF$')
text2html('Filling in the values gives:')
text2html('$ 8 \cdot 10^{-25} < 6.25 \cdot 10^{-24}$')
text2html('Thus using this technology we have a factor of 12.8 of room left for the noise requirements. ')

text2html('A plot of the total input flicker noise is shown below')
fig2html(fig_flicker,  500)

text2html('Using this information, we can conclude that the current technology is not a showstopper for the noise requirements')


