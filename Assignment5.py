# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 14:33:48 2021

@author: tomsa
"""

from SLiCAP import *
import globalVariables

######## Signal path part ########
makeNetlist('emptyCircuit.asc', 'Assignment 5 - Signal path design')            #Use an empty circuit to create the title page
i1 = instruction()
i1.setCircuit('emptyCircuit.cir')                                               #Set the empty circuit as active

head2html('Amplifier topology')
text2html('From the previous assignments, the conclusion could be made that an amplifier with only one stage is challenging. For that reason, a different topology for the amplifier has been chosen.')
text2html('To keep a reasonable amount of poles and zeros to work with, a 2-stage amplifier will be considered. Now only the type of stages will have to be determined.')
text2html('The result from the noise analysis states that CMOS technology can be used to meet the requirements. So much that there is still some room to play with the transistor parameters. Therefore, a CS-stage will do. To increase power efficiency and to suppress even functions, however, an anti-series stage can be substituded. Since the anti-series stage is able to generate the same level of noise as a CS-stage (with twice as wide transistors and a twice the drain current), the model for a CS-stage will be used in the noise analysis. Later on, during transient analysis, this model will be replaced with a complementary parallel circuit.')
text2html('The output stage is the next stage to determine. Again, from the previous assignments, the result is that the CMOS technology is able to meet the drive requirements. Again, a CS-stage can be used. However, due to a higher power efficiency, a complementary parallel stage (push-pull stage) will be considered.')
text2html('A convenient addition to choosing these two topologies is that the output of this two-stage amplifier is inverted in comparision to the input. The reason is that the push-pull stage inverts the signal while the differential pair does not inver the signal. This means that the output of the stages could directly drive a negative-feedback network.')

head2html('Feedback topology')
text2html('Next to the amplifier itself, negative feedback can be added. Advantages of using negative feedback are that the gain can be controlled precisely. In addition, choosing the correct feedback enables the amplifier to be resilient to ESD, which is one of the requirements.')
text2html('Like determined in the requirements, the innput antenna can be seen as an ideal voltage source with a capacitor in series to it. This means that either the voltage or the current of the input signal can be used. Next to the input, the output impedance of the amplifier should be fixed. Therefore, parameters A and B or C and D should be fixed.')
text2html('For the reason of simplicity and ESD protection, a single feedback loop is chosen and implemented as a capacitor from the output of the controller to the input of the controller, like shown in the following figure. Here, the parameters C and D are fixed.')
text2html('The total active antenna should have a gain of 1, so the value of the capacitor should have the value of $\ell * C_A$, so ' + str(globalVariables.L_A) + '*' + str(globalVariables.C_A) + ' = ' + str(globalVariables.L_A*globalVariables.C_A*1e12) + ' pF.')
img2html('topology.svg', 800)

head2html('Total signal path topology')
text2html('Now the different stages have been determined and the type of feedback has been chosen, the signal path topology is known. This signal path topology is unbiased still, but the general structure of the active amplifier is known.')
text2html('The amplifier consists of a differential pair as the input stage and a push-pull stage at the output. In addition, a capacitor is routed from the output to the input to create negative feedback. This is shown in the following figure.')
img2html('signalPath.svg', 800)

######## Input stage part ########
makeNetlist('InputStage.asc', 'Assignment 5 - Input stage design')
i1 = instruction()
i1.setCircuit('InputStage.cir')

text2html('Like mentioned in the requirements section, the noise is predominantly caused by the input stage of the amplifier. Since this amplifier will consist of two stages, the first will be investigated for its noise performance. For this amplifier, a differential pair is chosen as an input stage. Even though a differential pair is different from a single CS stage, its noise performance can be derrived from the performance of a single-CS stage.')

text2html('If a differential pair has transistors with twice the width of a single-CS stage and if the drain current through the differential pair is twice as large as the drain current of a single CS-stage, the noise characteristic of both devices are identical. Therefore, the noise characteristics of a single-CS stage is simulated. When the differential pair is implemented, the width of the transistors will be doubled and the pair will be biased so the drain current is twice as large as the noise performance results will give. The following figure shows the model used for noise-based calculations')

img2html('CS_noise.svg', 800)

head2html('Spectral noise requirements')
text2html('The requirements give a limit on the antenna-referred spectral noise density. At higher frequencies, this limit is constant, but at lower frequencies, this limit increases. The increment follows a $1/f^2$ characteristic. The frequency at which the frequency independent characteristic takes over from the frequency dependent characteristic is at: $$f_l = 200 [kHz]$$ This frequency is the corner frequency of the noise and is located at the point where the 1/f noise equals the floor noise.')

head2html('Optimal noise performance')
text2html('Since the input stage is driven from a capacitive voltage source, there is an optimum in noise performance. This optimum is found when the input capacitance of the stage $c_{iss}$ equals the source capacitance $C_s$. In this case, the source capacitance equals: $C_s = C_A + C_f$. Since $C_f = C_A \ell$, $C_s = C_A (1+\ell)$ and therefore the optimum is found when $$c_{iss} = C_A (1+\ell)$$')

