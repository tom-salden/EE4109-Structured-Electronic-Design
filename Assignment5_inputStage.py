# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 17:28:22 2021

@author: tomsa
"""

from SLiCAP import *
import globalVariables

######## Input stage part ########
makeNetlist('InputStage.asc', 'Assignment 5 - Input stage design')
i1 = instruction()
i1.setCircuit('InputStage.cir')
i1.defPar('IG',0)
i1.defPar('L_A', globalVariables.L_A)
i1.defPar('C_A', globalVariables.C_A)
i1.defPar('C_f', globalVariables.C_F)


text2html('Like mentioned in the requirements section, the noise is predominantly caused by the input stage of the amplifier. Since this amplifier will consist of two stages, the first will be investigated for its noise performance. For this amplifier, a differential pair is chosen as an input stage. Even though a differential pair is different from a single CS stage, its noise performance can be derrived from the performance of a single-CS stage.')

text2html('If a differential pair has transistors with twice the width of a single-CS stage and if the drain current through the differential pair is twice as large as the drain current of a single CS-stage, the noise characteristic of both devices are identical. Therefore, the noise characteristics of a single-CS stage is simulated. When the differential pair is implemented, the width of the transistors will be doubled and the pair will be biased so the drain current is twice as large as the noise performance results will give. The following figure shows the model used for noise-based calculations')

img2html('CS_noise.svg', 800)

head2html('Spectral noise requirements')
text2html('The requirements give a limit on the antenna-referred spectral noise density. At higher frequencies, this limit is constant, but at lower frequencies, this limit increases. The increment follows a $1/f^2$ characteristic. The frequency at which the frequency independent characteristic takes over from the frequency dependent characteristic is at: $$f_{\ell} = 200 [kHz]$$ This frequency is the corner frequency of the noise and is located at the point where the 1/f noise equals the floor noise.')

head2html('Optimal noise performance')
text2html('Since the input stage is driven from a capacitive voltage source, there is an optimum in noise performance. This optimum is found when the input capacitance of the stage $c_{iss}$ equals the source capacitance $C_s$. In this case, the source capacitance equals: $C_s = C_A + C_F$. Since $C_F = C_A \ell$, $C_s = C_A (1+\ell)$ and therefore the optimum is found when $$c_{iss} = C_A (1+\ell)$$')

head2html('Testing for feasibility')
text2html('Since there is an optimum in noise performance, a test can be done if the optimal design in terms of noise is still within the scope of the requirements. If this is the case, the design can continue and tweaks can be made to this first stage.')
text2html('After evaluating the expressions, the following design equation has to be valid for the stage to fall within noise requirements: $$\dfrac{3\cdot f_{\ell} \cdot C_s \cdot S_{v,floor}}{8 \cdot KF} > 1$$ Here, KF is a parameter that is defined by the technology of the transistor and $S_{v,floor}$ is the spectral density of the input-referred voltage noise of the active antenna. Like displayed in the section Design Overview, this noise floor equals:')

eqn2html('S_floor',globalVariables.S_floor,'V^2/Hz')

text2html('Filling in the parameters gives:')
KF_N18 = i1.getParValue('KF_N18')
f_l = 200e3
C_S = globalVariables.C_A * (1+globalVariables.L_A)

relMargin = (3*f_l*C_S*globalVariables.S_floor)/(8*KF_N18)

eqn2html('DesignMargin',relMargin)


i1.setSource('V1')
i1.setDetector('V_out')
i1.setSimType('numeric')
i1.setGainType('vi')
i1.setDataType('noise')
result = i1.execute()

# Prepare data for plotting with array stepping
widths     = [900*10**(-6), 700*10**(-6), 600*10**(-6), 400*10**(-6)] # CS-stage NMOS channel widths (900u, 600u, 400u, 300u)
stepArray  = [widths, [0 for i in range(len(widths))], [0 for i in range(len(widths))]]
CissTransistor = [0.1, 0.2, 0.3, 0.4, 0.5]

k = i1.getParValue('k')
T = i1.getParValue('T')

CA = globalVariables.C_A
Cf = globalVariables.C_F
Req = globalVariables.S_floor/(4*k*T*(1+globalVariables.L_A)**2)

htmlPage('Finding optimum with different widths')

for i in range(len(widths)):
    i1.defPar('W', stepArray[0][i])                     # Define a value for the width
    # Estimate the value for L such that c_iss = CA
    W = i1.getParValue('W')
    COVL = i1.getParValue('CGSO_N18')
    CGBO = i1.getParValue('CGBO_N18')
    COX  = i1.getParValue('C_OX_N18')
    L = sp.Symbol('L')
    Ctot = 2*COX*W*L/3+2*COVL*W+2*L*CGBO
    L = sp.solve(Ctot-C_S, L)[0]
    stepArray[1][i] = L
    i1.defPar('L', L)
    # Direct solution of ID from inoise(ID)-noiseFloor does not work!
    # Alternative:
    # Calculate the required equivalent total noise resistance R_eq and
    # solve ID from Req
    # Get symbolic expressions RN(ID) and gm(ID)
    i1.delPar('ID')
    RN = i1.getParValue('R_N_XU1')
    gm = i1.getParValue('g_m_XU1')
    # Calculate ReqID = the equivalent-input noise resistance as a funcion of ID 
    ReqID = (1 + C_S/(CA+Cf))**2/(gm**2*RN)
    # Now solve ID by equating both expressions: ReqID = Req
    #ID = sp.solve(ReqID - Req, sp.Symbol('ID'))[0]
    # fsolve from scipy is much faster than sp.solve (Sympy):
    # Convert the function ReqID(ID) - Req(ID) to a scipy function: funcID
    funcID = sp.lambdify(sp.Symbol('ID'), ReqID - Req)
    # Solve it with a nonzero startvalue
    ID = fsolve(funcID, 1e-38)[0]
    i1.defPar('ID', ID)
    # Define the value of ID
    stepArray[2][i] = ID
    # Put the data on a page
    head2html('Noise, W = {0:1.1e}'.format(W))
    result = i1.execute()
    params2html(i1.circuit)
    elementData2html(i1.circuit)
    # Print the results in the Console
    IC = i1.getParValue('IC_XU1')
    Ciss = i1.getParValue('c_iss_XU1')
    RN = i1.getParValue('R_N_XU1')
    f_ell = i1.getParValue('f_ell_XU1')
    noise2html(result)
    #print(i+1, ': W = {0:1.2e}, L = {1:1.2e}, ID = {2:1.2e}, S_f = {3:1.2e}, f_ell = {4:1.2e}, Ciss = {5:1.2e}, IC={6:1.2e}.'.format(W, L, ID, sp.N(sp.Subs(result.inoise, ini.frequency, 1e8),4), f_ell, Ciss, IC))
    CissTransistor[i] = Ciss

htmlPage('Simulation results')
head2html('Simulation results')
text2html('In the following figure, the properties of the different scaled input stages are shown. Like visible, the transistor current and length can be scaled in such a way that the different scaled transistors comply with the requirments.')

i1.setStepMethod('array')
i1.setStepVars(['W', 'L', 'ID'])
i1.setStepArray(stepArray)
i1.stepOn()
result = i1.execute()
figInoise = plotSweep('Inoise', 'Source-referred noise spectrum', result, 1e3, 1e8, 200, funcType = 'inoise', show=True)
fig2html(figInoise, 800)
stepArray2html(i1.stepVars, i1.stepArray)

text2html('This figure gives the optimal value of the noise performance of the input stage. Indeed, the noise floor is below $6.25 \times 10^{-18} \dfrac{V^2}{Hz}$, but this value is barely reached. On the other hand, the 1/f (or 1/f^2) noise easily meets the requirements. To give more headroom to the noise floor, different transistor parameters can be chosen. If the length of the transistor is decreased along with the drain current, the 1/f cutoff frequency will shift to a higher cutoff point and the noise floor will move down. Therefore, a transistor with the following parameters is used to give more headroom.')

# Final settings
L_input = 300*10**(-9)  #300n
W_input = 400*10**(-6)  #400u
ID_input = 1.8*10**(-3) #1.5m

i1.defPar('L', L_input)
i1.defPar('W', W_input)
i1.defPar('ID', ID_input)
i1.stepOff()
result = i1.execute()
figInoiseFinal = plotSweep('InoiseFinal', 'Inoise, L=300n, W=400u, ID=1.8m', result, 1e3, 1e8, 200, funcType = 'inoise', show=True)
fig2html(figInoiseFinal, 800)
Ciss = i1.getParValue('c_iss_XU1')

text2html('Another advantage of this is that the $C_{iss}$ of the input transistor will decrease in value. When attempting a frequency compenstation with a phantom zero on the input, a smaller $C_{iss}$ will place the added pole further making sure that it is not dominant. The difference in capacitance is as follows:')
eqn2html('Cissbefore', CissTransistor[2])
eqn2html('CurrentCiss', Ciss)