# -*- coding: utf-8 -*-
"""
Created on Fri Jan  5 14:22:07 2022

@author: tomsa
"""

from SLiCAP import *
import globalVariables
import compensationfunctions

makeNetlist('Assignment6-frequencyCompensation-rlphz.asc', 'Assignment 6 - Bandwidth limitation')
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
L_phz = 0

i1.defPar('Rphz',R_phz)         #Input Phantom Zero
i1.defPar('Lphz',L_phz)         #Output Phantom Zero

i1.setSimType('numeric')
i1.setSource('V1')
i1.setDetector('V_out')
i1.setLGref('Gm_M1_XU1')

text2html('Assignment 5 concluded with a design that should be able to drive the load with a noise level that is within the requirements and has a transfer that is compensated for the frequency characteristics. While this circuit should work as intended, the bandwidth of the circuit is very large. This means that out-of-band noise will bee transferred in addition to the signal itself. The phantom zero that was introduced for frequency compensation can also be used to limit the bandwidth so the circuit will be more fit for the application. In addition, a phantom zero can be introduced at the output of the circuit, providing a similar frequency compensation and bandwidth limitation.')

htmlPage('Bandwidth limitation with a phantom zero at the input')

head2html('Bandwidth limitation with a phantom zero at the input')
text2html('Even after frequency compensation, the bandwidth of the circuit is still too big, as the circuit has a cutoff frequency at around $1GHz$. By increasing the resistor value of the phantom zero at the input, the bandwidth can be limited somewhat.')

text2html('The reason this resistor allows for bandwidth limitation is that by increasing the value of the resistor, the pole created in the asymptotic gain and the zero created in the loopgain will move to a lower frequency. Next to this, the second pole is effected by the phantom zero resistance as well decreasing the loopgain poles product and thus the bandwidth.')

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
# figdBmag = plotSweep('plot1name', 'Uncompensated circuit', result, 1, 10e4, 100, sweepScale='M', funcType = 'dBmag', show=True)

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

text2html('The followig figure shows the behaviour of the circuit when the resistor value is increased.')
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
#fig2html(figdBmagfinalPhase,800)

head2html('Drawbacks')
text2html('A disadvantage of using this resistor for bandwidth limitation is that the resistor introduces noise. A resistor of $500 \Omega$ introduces $V_n=\sqrt{4kTR}=2.8nV/\sqrt{Hz}$. Since the noise floor should have a maximum of $2.5nV/\sqrt{Hz}$, this is too much. In addition, peaking around $3GHz$ is introduced. For that reason, bandwidth limitation using a phantom zero at the input is not used.')
text2html('The value of the resistor at the input will therefore have the value determined in Assignment 5, $13.81 \Omega$.')



htmlPage('Bandwidth limitation with a phantom zero at the output')
head2html('Bandwidth limitation with a phantom zero at the output')
text2html('Similar the phantom zero created at the input of the circuit, a phantom zero can be created at the output of the circuit as well. In contrast to a resistor used previously, the phantom zero is created by adding an inductor in series with the output of the stages. The circuit can be seen in')

img2html('Assignment6-frequencyCompensation-rlphz.svg', 800)

text2html('Like visible in the previous attempt on bandwidth limitation, the input phantom zero compensation was very effective. Unfortunately, when applying this technique peaking could easily occur at high frequencies. In addition, because of the use of a resistor, a lot of noise is added. To still limit the bandwidth, a different solution should be investigated. There are a lot of techniques to use for frequency compensation, however the methods other than phantom zero compensation create a non-ideality to limit the bandwidth. The phantom zero compensation uses an already present non-ideality and uses it to its advantage without affecting power usage or distortion too much. Therefore, phantom zero compensation is preferred as a method of bandwidth reduction. Because phantom zero compensation at the input of the amplifier is already applied and can not be increased a lot, phantom zero compensation at the output is still possible.')

R_phz = 13.81
L_phz = 8.5e-9                    #Can't be 0 for calculations
i1.defPar('Rphz',R_phz)         #Input Phantom Zero

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
figdBmag = plotSweep('plot1name-RL', 'Compensated circuit', result, 1, 10e4, 100, sweepScale='M', funcType = 'dBmag', show=True)

# Limit bandwidth to:
f_max = 30e6
L_max = sp.N((i1.getParValue('R1')+i1.getParValue('R2'))/(f_max*2*sp.pi))

i1.setStepVar('Lphz')
i1.setStepStart(L_phz)
i1.setStepStop(L_max)
i1.setStepNum(10)
i1.setStepMethod('log')
i1.stepOn()

i1.setGainType('gain')
gain = i1.execute()
figdBmagBWL = plotSweep('BWL-RL', 'Bandwidth limited amplifier', gain, 1, 10e4, 100, sweepScale='M', funcType = 'dBmag', show=True)

figdBmagBWLZoomed = plotSweep('BWLZoomed-RL', 'Bandwidth limited amplifier - zoomed', gain, 1, 50, 100, sweepScale='M', funcType = 'dBmag', show=True)

i1.setGainType('loopgain')
loopgain = i1.execute()
figdBmagBWLL = plotSweep('BWLloopgain-RL', 'Loop gain bandwidth limited amplifier', loopgain, 1, 10e4, 100, sweepScale='M', funcType = 'dBmag', show=True)

text2html('By first compensating the circuit with a phantom zero resistance at its input, the magnitude bode plot looks like this:')
fig2html(figdBmag, 800)
text2html('Now, an inductor in series with the load can be placed to create a phantom zero a the output. By increasing this inductance, the bandwidth of the amplifier decreases')
fig2html(figdBmagBWL, 800)
text2html('The requirements of the active antenna state that the -3dB frequency of the amplifier should be $30MHz$. Therefore, the compensation can be executed until the gain hits -9dB at $30MHz$. If the gain is zoomed in to the lower frequencies, it is visible that when the inductance is a little lower than $0.53\mu H$, the requirement is met. At this value, there will be a little peaking, as visible in the previous plot. Therefore, if an inductance of around $0.4 \mu H$ is chosen, the bandwidth is still limited and the peaking is a little less.')
fig2html(figdBmagBWLZoomed, 800)
text2html('Just as for the input phantom zero compensation, the zero in the loopgain will move to a lower value. This can be seen in the plot of the loopgain in the following figure. The effect of moving the zero to a lower frequency is that there is more loopgain available for lower frequencies. This is beneficial as it can decrease the influence of distortion.')
fig2html(figdBmagBWLL,800)
text2html('When a phantom zero resistance of $20 \Omega$ is chosen and a phantom zero inductance of $0.4 \mu H$ is chosen, it will give the following results:')

i1.defPar('Lphz', 4e-7)
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
figdBmagfinal = plotSweep('plot1name2-RL', 'Bandwidth limited amplifier', result, 1, 10e4, 100, sweepScale='M', funcType = 'dBmag', show=True)
figdBmagfinalPhase = plotSweep('plot1name3-RL', 'Bandwidth limited amplifier phase', result, 1, 10e4, 100, sweepScale='M', funcType = 'phase', show=True)
fig2html(figdBmagfinal,800)
fig2html(figdBmagfinalPhase,800)


text2html('Therfore, the conlcusion is that a phantom zero compensation at the input is added to compensate for the frequency behaviour and a phantom zero compensation at the output is added for bandwidth limitation. The value for the resistor is $13.81 \Omega$ and the value for the inductor is $0.4\mu H$.')

htmlPage('Pole analysis bandwidth limited antenna')
text2html('Indeed another pole is visible in the PZ analysis and since the phantom zero does not only affect the bandwidth but also the frequency response, the quality factor is changed.')
i1.setSimType('numeric')
i1.setSource('V1')
i1.setDetector('V_out')
i1.setLGref('Gm_M1_XU1')

i1.setGainType('loopgain')
i1.setDataType('pz')
pzResult = i1.execute()
polesLoopGain = pzResult.poles

i1.setDataType('laplace')
loopgain = i1.execute()
servoData = findServoBandwidth(loopgain.laplace)
Bf = servoData['lpf']

i1.setSimType('symbolic');
i1.setGainType('gain');
i1.setDataType('laplace');
i1.setSource('V1');
i1.setDetector('V_out');

i1.setSimType('numeric');
i1.setDataType('pz')
pz2html(i1.execute())