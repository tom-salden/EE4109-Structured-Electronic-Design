#Check de DC gain bij de PZ table, die staat nu nog op nan, met een nieuwe slicap versie proberen (V 1.1.1 werkt hiermee :D)

# -*- coding: utf-8 -*-

from SLiCAP import *
import globalVariables
#prj = initProject('Active Antenna Design - Design group 3')

######## Input stage part ########
makeNetlist('Assigment5_dual_stage_frequency.asc', 'Assignment 5 - Frequency analysis')
i2 = instruction()
i2.setCircuit('Assigment5_dual_stage_frequency.cir')

htmlPage("circuit data and circuit schematic")


i2.defPar('IG',0)
i2.defPar('L_A', globalVariables.L_A)
i2.defPar('C_A', globalVariables.C_A)
i2.defPar('C_F', globalVariables.C_F)

i2.defPar('W_DP', globalVariables.W_input)
i2.defPar('L_DP', globalVariables.L_input)
i2.defPar('ID_DP', globalVariables.ID_input)

i2.defPar('W_P', globalVariables.Wp_output)
i2.defPar('W_N', globalVariables.Wn_output)

i2.defPar('L_N', globalVariables.Ln_output)
i2.defPar('L_P', globalVariables.Lp_output)


i2.defPar('ID_N', globalVariables.ID_n)
i2.defPar('ID_P', globalVariables.ID_p)
i2.defPar('R_C', 50)
i2.defPar('R_phz', 0)


head2html('Two-stage circuit analysis')

#img2html('Assigment5_dual_stage_frequency.PNG', 800)
img2html('frequencyCompensation-rphz.svg', 800)

elementData2html(i2.circuit)
params2html(i2.circuit)

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
#text2html('To be added in the final report') 


i2.setSimType('numeric')
i2.setSource('V2')
i2.setDetector('V_out')
i2.setLGref('Gm_M1_XU1')

i2.setGainType('loopgain')
i2.setDataType('pz')
pzResult = i2.execute()
polesLoopGain = pzResult.poles

htmlPage('Bandwidth and ploles and zeros of this solution' )
text2html('After applying the values for this circuit (the resistor $R_{phz}$ is initially set to 0), the bandwidth should be determined. If this bandwith is large enough, the amplifier can be used in this specific application. If it is too large, some bandwidth limitation techniques might have to be applied. The value of the bandwidth is as follows:')

i2.setDataType('laplace')
loopgain = i2.execute()
servoData = findServoBandwidth(loopgain.laplace)
Bf = servoData['lpf']
print('Bf: {0:1.2e}'.format(float(Bf)))
eqn2html('B_f',Bf*1e-9,'GHz')

text2html('The bandwidth requirement of the amplifier was listed at $30MHz$, the achieved bandwidth is much higher thus the design is sufficient for the application.')
text2html('In addition to the frequency derivation, the poles and zeros can be determined. They are displayed below:')

i2.setSimType('numeric')
i2.setSource('V2')
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

text2html('From theses we can immediately see that freqency compensation is needed since the Q is much higher than the desired 0.707 for a MFM characteristic.')
text2html('In the next page the bode plots are shown where the peaking due to the high Q is clearly visible, therefore frequency compensation is needed.')

htmlPage('Bode plots')
head2html('Bode plots showing the gain transfer')
text2html('Visible in the following bode plots is the frequency behaviour. The plot shows that the frequency behaviour of the amplifier is not flat until a frequency around $30 MHz$ is reached. This is still in line with the requirements.')
#result = [asymptotic, gain, loopgain, servo, direct]
result = [gain]
figdBmag = plotSweep('dBmag', 'dB magnitude', result, 10, 10e4, 100, sweepScale='M', funcType = 'dBmag', show=True)
figPhase = plotSweep('phase', 'Phase', result, 10, 10e4, 100, sweepScale='M', funcType = 'phase', show=True)
fig2html(figdBmag, 800)
fig2html(figPhase, 800)

head2html('Bode plots showing all relavant transfers')
result = [asymptotic, gain, loopgain, servo, direct]
figdBmag = plotSweep('dBmag2', 'dB magnitude2', result, 10, 10e4, 100, sweepScale='M', funcType = 'dBmag', show=True)
figPhase = plotSweep('phase2', 'Phase2', result, 10, 10e4, 100, sweepScale='M', funcType = 'phase', show=True)
fig2html(figdBmag, 800)
fig2html(figPhase, 800)

#plotPZ

# Select the dominant poles
dominantPoles = []
for pole in polesLoopGain:
    # Poles and zeros are always in rad/s
    if ini.Hz:
        pole = sp.N(pole/2/sp.pi)
    if sp.Abs(pole) < 2*Bf:
        dominantPoles.append(pole)
        print('Pole: {0:1.2e}'.format(float(sp.N(pole))))

# Calculate the compensation if there are two dominant poles        
if len(dominantPoles) == 2:
    f_phz = Bf**2/(np.sqrt(2)*Bf + dominantPoles[0] + dominantPoles[1])
    R_phz = 1/(2*np.pi*f_phz*i2.getParValue('C_A'))
    i2.defPar('R_phz', R_phz)
    print('Rphz', R_phz)
    print('fphz', f_phz)

# Plot the transfer
i2.setGainType('gain')
gain = i2.execute()
#htmlPage('Bode plots of the compensated antenna')
#figdBmag = plotSweep('dBmagPhZ1', 'dB magnitude compensated active antenna', gain, 10, 10e4, 100, sweepScale='M', funcType = 'dBmag', show=True)
#figPhase = plotSweep('phasePhZ1', 'Phase compensated active antenna', gain, 10, 10e4, 100, sweepScale='M', funcType = 'phase', show=True)
#fig2html(figdBmag, 800)
#fig2html(figPhase, 800)

# Plot the poles of the gain as a function of the compensation resistance
i2.setDataType('poles')
i2.setStepVar('R_phz')
i2.setStepStart(0.5*R_phz)
i2.setStepStop(1.5*R_phz)
i2.setStepNum(15)
i2.setStepMethod('lin')
i2.stepOn()
figPolesAll    = plotPZ('polesGainPhZ1', 'poles of the gain', i2.execute(), show=True)
figPolesSquare = plotPZ('polesGainPhZ1zoom', 'poles of the gain', i2.execute(), xmin=-3, xmax=0, ymin=-1.5, ymax=1.5, xscale='G', yscale='G', show=True)
htmlPage('Nyquist plots to determine $R_{phz}$')
fig2html(figPolesAll, 800)
fig2html(figPolesSquare, 800)
text2html('In these figures the nyquist diagram is shown of the amplifier, here the calculated value of $R_{phz}$ is equal to $11.89\Omega$ using the fllowing 2 equtions:' )
text2html('$R_{phz}=\dfrac{1}{2\cdot \pi \cdot f_{phz} \cdot C_{A}}$')
text2html('$f_{phz} = \dfrac{B_{f}^{2}}{ \sqrt(2 B_{f}) + p_{1}+ p_{2}}$')
text2html('Here $p_{1}$ and $p_{2}$ are the 2 dominant poles of the circuit.')

text2html('In the nyquist plot the start value is set to $0.5 \cdot R_phz$ and this value is swept till $1.5 \cdot R_phz$ in 15 steps.')
text2html('From the plot we get for the 10th step a pole position at almost $45 ^{\circ}$ angle is reached which infers a MFM characteristic, this is thus at a value of $R_{phz}=13.9\Omega$.')
i2.stepOff()
print(R_phz)

htmlPage('Pole analysis compensated antenna')

i2.defPar('R_phz', 13.9)

text2html('Now the value of $13.9\Omega$ is substituted in $R_{phz}$ and a frequency analysis is run again. Below the locations of the new poles and zeros is shown and the Q factor.')
text2html('Now the Q factor is almost excatly at 0.707 for a MFM characteristic as intended, in the next page the bode plot is shown where the (almost) flat passband transfer is shown.')

i2.setSimType('numeric')
i2.setSource('V2')
i2.setDetector('V_out')
i2.setLGref('Gm_M1_XU1')

i2.setGainType('loopgain')
i2.setDataType('pz')
pzResult = i2.execute()
polesLoopGain = pzResult.poles

i2.setDataType('laplace')
loopgain = i2.execute()
servoData = findServoBandwidth(loopgain.laplace)
Bf = servoData['lpf']

i2.setSimType('symbolic');
i2.setGainType('gain');
i2.setDataType('laplace');
i2.setSource('V2');
i2.setDetector('V_out');

i2.setSimType('numeric');
i2.setDataType('pz')
pz2html(i2.execute())



htmlPage('Bode plots compensated antenna')
i2.setDataType('laplace')
i2.setGainType('gain')
gain = i2.execute()
figdBmag = plotSweep('dBmagPhZ1', 'dB magnitude compensated active antenna', gain, 10, 10e4, 100, sweepScale='M', funcType = 'dBmag', show=True)
figPhase = plotSweep('phasePhZ1', 'Phase compensated active antenna', gain, 10, 10e4, 100, sweepScale='M', funcType = 'phase', show=True)
fig2html(figdBmag, 800)
fig2html(figPhase, 800)