# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 14:33:48 2021

@author: tomsa
"""

from SLiCAP import *

makeNetlist('emptyCircuit.asc', 'Assignment 5 - Signal path design')
i1 = instruction()
i1.setCircuit('emptyCircuit.cir')

head2html('Amplifier topology')
text2html('From the previous assignments, the conclusion could be made that an amplifier with only one stage is challenging. For that reason, a different topology for the amplifier has been chosen.')
text2html('To keep a reasonable amount of poles and zeros to work with, a 2-stage amplifier will be considered. Now only the type of stages will have to be determined.')
text2html('The result from the noise analysis states that CMOS technology can be used to meet the requirements. So much that there is still some room to play with the transistor parameters. Therefore, a CS-stage will do. To increase power efficiency and to suppress even functions, however, an anti-series stage can be substituded. Since the anti-series stage is able to generate the same level of noise as a CS-stage (with twice as wide transistors and a twice the drain current), the model for a CS-stage will be used in the noise analysis. Later on, during transient analysis, this model will be replaced with a complementary parallel circuit.')
text2html('The output stage is the next stage to determine. Again, from the previous assignments, the result is that the CMOS technology is able to meet the drive requirements. Again, a CS-stage can be used. However, due to a higher power efficiency, a complementary parallel stage (push-pull stage) will be considered.')
text2html('A convenient addition to choosing these two topologies is that the output of this two-stage amplifier is inverted in comparision to the input. This means that the output of the stages could directly drive a negative-feedback network.')

head2html('Feedback topology')
text2html('Next to the amplifier, itself, negative feedback ')