from SLiCAP import *

fileName = 'CSstage.txt'
color = 'c'
dB=False

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

fileName = 'assignment1 - DriveCapability.txt'
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
LTtraceOut = [{'LTtrace': LTtrace}]
