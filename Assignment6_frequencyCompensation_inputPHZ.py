# -*- coding: utf-8 -*-
"""
Created on Fri Jan  5 14:22:07 2022

@author: tomsa
"""

from SLiCAP import *
import globalVariables

makeNetlist('Assignment6-frequencyCompensation-rphz.asc', 'Assignment 6 - Frequency adjustments')
i1 = instruction()
i1.setCircuit('Assignment6-frequencyCompensation-rphz.cir')

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
i1.defPar('ID_P', '-300m')
i1.defPar('R1', 50)
i1.defPar('R2', 50)

R_phz = 1

i1.defPar('Rphz',R_phz)         #Input Phantom Zero

head2html('Frequency compensation')
text2html('Like visible in the design of Assignment 5, there is no real case of peaking in the frequency range. Therefore, frequency compensation will not increase the frequency performance by much.')

head2html('Bandwidth limitation')
text2html('Contrary to the frequency compensation, the bandwidt of the circuit is still too big, as the circuit has a cutoff frequency of around 300 MHz. This bandwidth can be limited using techniques like adding a phantom zero on the input or output. The following image shows how a phantom zero is added to the input of the circuit, allowing for bandwidth limitation.')
img2html('frequencyCompensation-rphz.svg', 1000)

text2html('The reason this resistor allows for bandwidth limitation is that by increasing the value of the resistor, the pole created in the asymptotic gain and the zero created in the loopgain will move to a lower frequency. Next to this, the second pole is effected by the phantom zero resistance as well decreasing the loopgain poles product and thus the bandwidth.')

i1.setSimType('numeric')
i1.setSource('V1')
i1.setDetector('V_out')
i1.setLGref('Gm_M1_XU1')

i1.setDataType('laplace')
i1.setGainType('gain')
gain = i1.execute()

i1.setGainType('loopgain')
loopgain = i1.execute()

i1.setGainType('asymptotic')
asymptotic = i1.execute()

i1.setGainType('servo')
servo = i1.execute()

i1.setGainType('direct')
direct = i1.execute()

result = [asymptotic, gain, loopgain, servo, direct]
figdBmag = plotSweep('plot1name', 'Uncompensated circuit', result, 1, 10e4, 100, sweepScale='M', funcType = 'dBmag', show=True)

# Limit bandwidth to:
f_max = 30e6
R_max = sp.N(1/(f_max*2*sp.pi*globalVariables.C_A))

i1.setStepVar('Rphz')
i1.setStepStart(R_phz)
i1.setStepStop(R_max)
print(R_max)

i1.setStepNum(10)
i1.setStepMethod('log')
i1.stepOn()

i1.setGainType('gain')
gain = i1.execute()

figdBmagBWL = plotSweep('BWL', 'Bandwidth limited amplifier', gain, 1, 10e4, 100, sweepScale='M', funcType = 'dBmag', show=True)

figdBmagBWLZoomed = plotSweep('BWLZoomed', 'Bandwidth limited amplifier - zoomed', gain, 1, 50, 100, sweepScale='M', funcType = 'dBmag', show=True)

i1.setGainType('loopgain')
loopgain = i1.execute()
figdBmagBWLL = plotSweep('BWLloopgain', 'Loop gain bandwidth limited amplifier', loopgain, 1, 10e4, 100, sweepScale='M', funcType = 'dBmag', show=True)


text2html('The following figure shows the magnitude part of the bode plot for the circuit without bandwidth limitation.')
fig2html(figdBmag, 800)
text2html('However, when increasing the value of the resistor, the bandwidth of the amplifier deceases. This is shown in the next figure:')
fig2html(figdBmagBWL, 800)
text2html('The requirements of the active antenna state that the -3dB frequency of the amplifier should be $30MHz$. Therefore, the compensation can be executed until the gain hits -9dB at $30MHz$. If the gain is zoomed in to the lower frequencies, it is visible that when the resistance is a little lower than $530 \Omega$, the requirement is met.')
fig2html(figdBmagBWLZoomed, 800)
text2html('As already mentioned, the zero in the loopgain will move to a lower value. This can be seen in the plot of the loopgain in the following figure. The effect of moving the zero to a lower frequency is that there is more loopgain available for lower frequencies. This is beneficial as it can decrease the influence of distortion.')
fig2html(figdBmagBWLL,800)

text2html('When a phantom zero resistance of $500 \Omega$ is chosen, it will give the following results:')

i1.defPar('Rphz', 500)
i1.stepOff()

i1.setDataType('laplace')
i1.setGainType('gain')
gain = i1.execute()
i1.setGainType('loopgain')
loopgain = i1.execute()
i1.setGainType('asymptotic')
asymptotic = i1.execute()
i1.setGainType('servo')
servo = i1.execute()
i1.setGainType('direct')
direct = i1.execute()

result = [asymptotic, gain, loopgain, servo, direct]
figdBmagfinal = plotSweep('plot1name2', 'Bandwidth limited amplifier', result, 1, 10e4, 100, sweepScale='M', funcType = 'dBmag', show=True)
figdBmagfinalPhase = plotSweep('plot1name3', 'Bandwidth limited amplifier phase', result, 1, 10e4, 100, sweepScale='M', funcType = 'phase', show=True)
fig2html(figdBmagfinal,800)
fig2html(figdBmagfinalPhase,800)

head2html('Drawbacks')
text2html('A disadvantage of using this resistor for bandwidth limitation is that the resistor introduces noise. A resistor of $500 \Omega$ introduces $V_n=\sqrt{4kTR}=2.8nV/\sqrt{Hz}$. Since the noise floor should have a maximum of $2.5nV/\sqrt{Hz}$, this is too much. Of course, the noise from the amplifier itself still has to be added. To make the noise contribution less significant, a resistor of $50 \Omega$ is chosen to have only a small noise contribution but still limit the bandwidth somewhat.')