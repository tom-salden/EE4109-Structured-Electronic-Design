# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 12:19:53 2021

@author: Design Group 3
"""

from SLiCAP import *

#Create new page with the circuit
i1 = instruction()
i1.setCircuit('assignment1 - DriveCapability.cir')
img2html('assignment1 - DriveCapability.svg', 900)

head2html('Drive capability of a CS stage')
text2html('The most uncomplicated method of creating an amplifier is to use a single CS stage. However, in order to test if this one stage is able to satisfy the requirements, some drive capability and noise simulations have to be done. The stage has to be able to drive the load without adding too much noise.')
text2html('First, the correct biasing needs to be determined to fulfil the design requirements. The active antenna needs to deliver $0dbm$ ($1mW$) into $50 \Omega$. The RMS voltage should be $V_{RMS}=\sqrt{P \cdot R} = 233 mV$. Now the peak value is obtained by multiplication with the crest factor $V_{PP}=\sqrt{2}\cdot 233mV = 316 mV$.')
text2html('Thus the CS stage needs to drive $316 mV$ at the output. The first method is using brute force by placing an additional $50\Omega$ resistor in series witth the amplifier output. Then the total impedace seen at the output would be $100\Omega$. In order to fullfil the $316mV$ requirement we need a current of $$I_D= 316mV/50\Omega \approx 6.4mA$$')