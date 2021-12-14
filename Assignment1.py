# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 12:19:53 2021

@author: Design Group 3
"""


from SLiCAP import *
from pythonfunctions import *

#Create new page with the circuit
i1 = instruction()
i1.setCircuit('assignment1 - DriveCapability.cir')

htmlPage('Drain voltage and current')

img2html('assignment1 - DriveCapability.svg', 900)

head2html('Drive capability of a CS stage')
text2html('The most uncomplicated method of creating an amplifier is to use a single CS stage. However, in order to test if this one stage is able to satisfy the requirements, some drive capability and noise simulations have to be done. The stage has to be able to drive the load without adding too much noise.')
text2html('First, the correct biasing needs to be determined to fulfil the design requirements. The active antenna needs to deliver $0dbm$ ($1mW$) into $50 \Omega$. The RMS voltage should be $V_{RMS}=\sqrt{P \cdot R} = 233 mV$. Now the peak value is obtained by multiplication with the crest factor $V_{PP}=\sqrt{2}\cdot 233mV = 316 mV$.')
text2html('Thus the CS stage needs to drive $316 mV$ at the output. The first method is using brute force by placing an additional $50\Omega$ resistor in series witth the amplifier output. Then the total impedace seen at the output would be $100\Omega$. In order to fullfil the $316mV$ requirement we need a current of $$I_D= 316mV/50\Omega = 6.32mA$$ This means about $6.4mA$ is necessary to drive the output stage.')
text2html('On the other hand, the CS stage needs to drive $-316 mV$ at the output as well. Using the same brute force method, the drain-source voltage of the stage should drive $2\cdot 316 mV$. This means that the voltage necessary to drive the load is: $$V_D = 632 mV$$')

text2html('Using the testbench provided for the driving capability, the following output characteristics are obtained for the drive voltage.')

#Trace the voltage characteristic from the LT-Spice export
LTDriveVoltage, empty = LTspiceDC2SLiCAPtraces('assignment1 - DriveCapability.txt')

figDrive_out = plot('DriveVoltageLoad', 'The voltage over the 50 ohm load for a swept gate voltge', 'lin', LTDriveVoltage, xName='$V_{G}$', xUnits='$V$', yName='$V_{out}$', yUnits='$V$', show=True)

fig2html(figDrive_out, 600, caption='The voltage over the 50 ohm load for a swept gate voltge.')

htmlPage('Device geometry')

head2html('Device geometry determination')

text2html('After finding the minimum drain voltage and current, the geometry of the device needs to be investigated. To start off, a lenght of $L=180nm$ is suggested as this is the minimal length of the transistor. Now, in order to select the width (or the multiplication factor M), the output characteristics for varying M with $W= 50\mu m$ can be plotted:')

img2html('assignment1 - Multiplyer.svg', 900)

text2html('From these result the effect of increasing the width of the transistor becomes visible. Increasing the width will increase the current through the transistor and thus the transconductance gm will also increase. From the obtained figure we can see that for low values such as $M=1$ the circuit is not able to achieve the desired output voltage driving capabilities. For $M>12$ we obtain $V_{out} \geq 620 mV$. Which seems to be sufficient for the design.')

htmlPage('Characterisation of chosen parameters')
head2html('$f_{T} vs I_{D}$')
text2html('Next is obtaining a plot of $f_{T} vs I_{D}$. Therefore the $f_{T}$ testbench is used using the obtained values for $V_{D}, M, L$ and running the simulation from $0mA$ to $3.2mA$. Now adding the $100\Omega$ load in series with $V_{D}$ and running the simulation gives the following plot for $f_{T}$.')

LTft, empty = LTspiceDC2SLiCAPtraces('NMOS-fT-testbench.log.txt')

figfT_out = plot('FtIdPlot', 'The $f_{T}$ versus the $I_{D}$', 'lin', LTft, xName='$I_{D}$', xUnits='$A$', yName='$f_{T}$', yUnits='$Hz$', show=True)

fig2html(figfT_out, 600, caption='The $f_{T}$ versus the $I_{D}$')

head2html('$g_{m}$')
text2html('Next is plotting the $g_{m}$, therefore the $g_{m}$ testbench is used where all values of the previous parts of the assignment have been substituted. And the $100 \Omega$ load is connected. Now plotting $g_{m} vs I_{D}$ gives the following result:')

LTgm, empty = LTspiceDC2SLiCAPtraces('NMOS-gm-testbench.txt')

figgm_out = plot('gmPlot', 'The $g_{m}$ versus the $I_{D}$', 'lin', LTgm, xName='$I_{D}$', xUnits='$A$', yName='$g_{m}$', yUnits='$1/\Omega$', show=True)

fig2html(figgm_out, 600, caption='The $g_{m}$ versus the $I_{D}$')


text2html('Measuring the $g_m$ at $I_D = 6.4 mA$ gives approximately $g_m = 94 mS$.')

htmlPage('Other methods')
text2html('For the other 2 methods the same method as previously described can be used. When the amplifier has a current output and a $50\Omega$ resistor is placed in parallel, we get a total resistance of $25 \Omega$ instead of the previous $100 \Omega$ used for the voltage output. And for the elegant solution using a dual loop feedback we simply only use a $50 \Omega$ total resistance at the output and obtain the parameters.')