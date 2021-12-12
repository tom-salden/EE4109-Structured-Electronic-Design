# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#from SLiCAP import *



from SLiCAP import *


makeNetlist('emptyCircuit.asc', 'Assignment 4 - Complementary-parallel CS output stage');
i1 = instruction();
i1.setCircuit('emptyCircuit.cir')

text2html('In this part a complementary-parallel CS output stage for the active antenna is characterized, below the test circuit of such a stage is shown where also the biasing is presented.')
img2html('ABstage.PNG', 1000)
text2html('In the circuit the gate bias of the NMOS and PMOS transistors is swept in order to obtain the common-mode and differential mode characteristics of the class AB output stage.')
text2html('It is important that the output stage can drive the 100 $\Omega$ load, for this we need a output voltage level of 640$mV$ and a current of 3.2 $mA$.')

text2html('For the dimensions of the NMOS transistor the obtained values of the previous assigment are used these are:')
text2html('$W_{NMOS}$ = 50um')
text2html('$L_{NMOS}$ = 180nm')
text2html('$M_{NMOS}$ = 2')

text2html('Now to first obtain the approritae dimension of the PMOS transistor we use the tip given in chapter 6 of the book that the width of the PMOS of the stage should be taken 3.5 times larger compared to the NMOS, since the hole mobility is lower than the electron mobility.')
text2html('$W_{PMOS}$ = 35um')
text2html('$L_{PMOS}$ = 180nm')
text2html('$M_{PMOS}$ = 10')




text2html('Next is the the quiescent bias current of the stage, at zero input signal,the common-mode current equals the quiescent operating current.')
text2html('for this the following equation given in chapter 6 can be used.')
text2html('$$\dfrac{I_{o}}{I_{Q}} = 2 sinh \dfrac{V_{i}}{n U_{T}}$$')
text2html('Here n is the substrate factor which is for weak inversion equal to n=2, and $U_{T}$ is the thermal voltage.')

text2html('First we plot the (differential) output load voltage of the stage.')
img2html('DM.PNG', 1000)
text2html('Here the quiescent current is swept between $100mA$ and $1A$. ')
text2html('From this plot we want to obtain a linear transfer characteristics and to fulfill the drive capability.')
text2html('The result for a  quiescent operating current of 300 $mA$ seems to give a good linear transfer, which means low crossover distortion also the 640 $mV$ requirement is met with this value.')

text2html('Below the simulation results of the provided test circuit (corresponsing to the circuit given above) is shown, here the common mode output current is plotted againt the input voltage.')
img2html('CM_plot.PNG', 1000)

text2html('For this plot it is important that there is no deadzone present, which leads to more distortion and a reduction in gain.')
text2html('Again for the 300$mA$ there is no deadzone visible and the drive requirement of 3.2$mA$ is also met.')
