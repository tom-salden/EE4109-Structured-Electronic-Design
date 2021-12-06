# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 12:41:02 2021

@author: tomsa
"""
from SLiCAP import *

def LTspiceDC2SLiCAPtraces(fileName, dB=False, color='c'):
    """
    This function converts the results of a single-run LTspice DC analysis 
    into two traces (mag, phase) that can be added to SLiCAP plots.
    
    :param fileName: Name of the file. The file should be located in 
                     the ditectory given in *ini.txtPath*.
    :type fileName:  str
    
    :param dB: True if the trace magnitude should be in dB, else False.
               Default value = False
    :type dB: bool
    
    :param color: Matplotlib color name. Valid names can be found at:
                  https://matplotlib.org/stable/gallery/color/named_colors.html
                  Default value is cyan (c); this does not correspond with one
                  of the standard gain colors of the asymptotic-gain model.
    :type color:  str
    
    :return: a list with two trace dicts, magnitude and phase, respectively.
    :rtype: list
    
    :Example:
        
    >>> LTmag, LTphase = LTspiceAC2SLiCAPtraces('LTspiceACdata.txt')
    """
    try:
        f = open(ini.txtPath + fileName, 'r', encoding='utf-8', errors='replace')
        lines = f.readlines()
        f.close()
    except:
        print('Cannot find: ', fileName)
        lines = []
    xAxis = []
    yAxis = []
    for i in range(len(lines)):
        if i != 0:
            line = lines[i].split()
            xAxis.append(eval(line[0]))
            yAxis.append(eval(line[1]))
    LTtrace = trace([xAxis, yAxis])
    LTtrace.label = 'LTtrace'
    LTtrace.color = color
    LTtraceOut = [{'LTtrace': LTtrace}, {'emptyTrace': LTtrace}]
    return LTtraceOut

def LTspiceAC2SLiCAPtraces(fileName, dB=False, color='c'):
    """
    This function converts the results of a single-run LTspice AC analysis 
    into two traces (mag, phase) that can be added to SLiCAP plots.
    
    :param fileName: Name of the file. The file should be located in 
                     the ditectory given in *ini.txtPath*.
    :type fileName:  str
    
    :param dB: True if the trace magnitude should be in dB, else False.
               Default value = False
    :type dB: bool
    
    :param color: Matplotlib color name. Valid names can be found at:
                  https://matplotlib.org/stable/gallery/color/named_colors.html
                  Default value is cyan (c); this does not correspond with one
                  of the standard gain colors of the asymptotic-gain model.
    :type color:  str
    
    :return: a list with two trace dicts, magnitude and phase, respectively.
    :rtype: list
    
    :Example:
        
    >>> LTmag, LTphase = LTspiceAC2SLiCAPtraces('LTspiceACdata.txt')
    """
    try:
        f = open(ini.txtPath + fileName, 'r', encoding='utf-8', errors='replace')
        lines = f.readlines()
        f.close()
    except:
        print('Cannot find: ', fileName)
        lines = []
    freqs = []
    mag   = []
    phase = [] 
    for i in range(len(lines)):
        if i != 0:
            line = lines[i].split()
            if ini.Hz:
                freqs.append(eval(line[0]))
            else:
                freqs.append(eval(line[0])*2*np.pi)
            dBmag, deg = line[1].split(',')
            dBmag = eval(dBmag[1:-2])
            deg = eval(deg[0:-2])
            if not dB:
                mag.append(10**(dBmag/20))
            else:
                mag.append(dBmag)
            if ini.Hz:
                phase.append(deg)
            else:
                phase.append(np.pi*deg/180)
    LTmag = trace([freqs, mag])
    LTmag.label = 'LTmag'
    LTmag.color = color
    LTphase = trace([freqs, phase])
    LTphase.label = 'LTphase'
    LTphase.color = color
    traces = [{'LTmag': LTmag}, {'LTphase': LTphase}]
    return traces