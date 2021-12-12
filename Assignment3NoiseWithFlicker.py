#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Noise analysis without flicker
"""
from SLiCAP import *

i1 = instruction()
i1.setCircuit('Assignment3_nobias.cir')
# create an html page for the results
#htmlPage('Flicker noise analysis')

text2html('We again use the same circuit')
img2html('Assignment3.png', 700)

# calculate source referred noise spectrum
i1.setSource('V1')
i1.setDetector('V_out')
i1.setGainType('vi')
i1.setDataType('Noise')
i1.setSimType('numeric')
# i1.setStepMethod('lin')
# i1.setStepVar('W')
# i1.setStepStart(10e-6)
# i1.setStepStop(1e-3)
# i1.setStepNum(10)
# i1.stepOn()
noiseResult = i1.execute()
head2html('Source referred noise')

text2html('Here is the source refered noise, now with 1/f noise');
figSin = plotSweep('Noise_with_flicker','Input noise spectrum (10 kHz - 30 GHz)', noiseResult,
                   10e3, 30e9, 100, funcType='inoise', show = True)
fig2html(figSin,  500)
text2html('We can now clearly see the effect of the 1/f noise')

