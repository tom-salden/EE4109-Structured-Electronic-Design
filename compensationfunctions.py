from SLiCAP import *
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg


def banddwidthCalculation(i1):
    #Calculate achievable bandwidth
    i1.setDataType('laplace')
    loopgain = i1.execute()
    servoData = findServoBandwidth(loopgain.laplace)
    Bf = servoData['lpf']
    print('Bf: {0:1.2e}'.format(float(Bf)))
    return Bf


def pzenbodePlotter(i1, plot1name, plot1descr, plot2name, plot2descr, plot):
    i1.setGainType('gain')
    i1.setDataType('pz')
    pz2html(i1.execute())
    i1.setDataType('laplace')
    gain = i1.execute()

    i1.setGainType('loopgain')
    i1.setDataType('pz')
    pz2html(i1.execute())

    if (plot == True):
        i1.setDataType('laplace')
        loopgain = i1.execute()

        i1.setGainType('asymptotic')
        asymptotic = i1.execute()

        i1.setGainType('servo')
        servo = i1.execute()

        i1.setGainType('direct')
        direct = i1.execute()

        result = [asymptotic, gain, loopgain, servo, direct]
        figdBmag = plotSweep(plot1name, plot1descr, result, 10, 10e4, 100, sweepScale='M', funcType = 'dBmag', show=True)
        figPhase = plotSweep(plot2name, plot2descr, result, 10, 10e4, 100, sweepScale='M', funcType = 'phase', show=True)
        fig2html(figdBmag, 800)
        fig2html(figPhase, 800)

def pzenbodePlotter2(i1, plot1name, plot1descr, plot2name, plot2descr):
    i1.setGainType('gain')
    i1.setDataType('pz')
    i1.setDataType('laplace')
    gain = i1.execute()

    i1.setGainType('loopgain')
    i1.setDataType('pz')
    i1.setDataType('laplace')
    loopgain = i1.execute()

    i1.setGainType('asymptotic')
    asymptotic = i1.execute()

    i1.setGainType('servo')
    servo = i1.execute()

    i1.setGainType('direct')
    direct = i1.execute()

    result = [asymptotic, gain, loopgain, servo, direct]
    figdBmag = plotSweep(plot1name, plot1descr, result, 10, 10e4, 100, sweepScale='M', funcType = 'dBmag', show=True)
    figPhase = plotSweep(plot2name, plot2descr, result, 10, 10e4, 100, sweepScale='M', funcType = 'phase', show=True)
    fig2html(figdBmag, 800)
    fig2html(figPhase, 800)

def rootLocusPlotter(i1, plot1name, plot1descr, plot2name, plot2descr, plot2minx, plot2maxx, plot2miny, plot2maxy, stepvar, stepvarnum):
    #plot the poles of the gain as a function of the compensation resistance
    i1.setGainType('gain')
    i1.setDataType('poles')
    i1.setStepVar(stepvar)
    i1.setStepStart(0.5*stepvarnum)
    i1.setStepStop(2*stepvarnum)
    i1.setStepNum(10)
    i1.setStepMethod('lin')
    i1.stepOn()
    figPolesAll = plotPZ(plot1name, plot1descr, i1.execute(), show=True)
    figPolesSquare = plotPZ(plot2name, plot2descr, i1.execute(), xmin=plot2minx, xmax = plot2maxx, ymin = plot2miny, ymax = plot2maxy, show=True)

    fig2html(figPolesAll, 800)
    fig2html(figPolesSquare, 800)
    return figPolesSquare

def rootLocusPlotterStartStop(i1, plot1name, plot1descr, plot2name, plot2descr, plot2minx, plot2maxx, plot2miny, plot2maxy, stepvar, stepstart, stepstop):
    #plot the poles of the gain as a function of the compensation resistance
    i1.setGainType('gain')
    i1.setDataType('poles')
    i1.setStepVar(stepvar)
    i1.setStepStart(stepstart)
    i1.setStepStop(stepstop)
    i1.setStepNum(10)
    i1.setStepMethod('lin')
    i1.stepOn()
    figPolesAll = plotPZ(plot1name, plot1descr, i1.execute(), show=True)
    figPolesSquare = plotPZ(plot2name, plot2descr, i1.execute(), xmin=plot2minx, xmax = plot2maxx, ymin = plot2miny, ymax = plot2maxy, show=True)

    fig2html(figPolesAll, 800)
    fig2html(figPolesSquare, 800)
    return figPolesSquare


def plotMetHoek(self):
    """
    Creates the figure, displays it if SLiCAPplots.figure.show == True and
    saves it to disk.
    """
    ## courtesy from the SLiCAP library :) 
    axes = np.array(self.axes)
    try:
        rows, cols = axes.shape
    except:
        print('Attribute of <figure>.axes must be a list of lists or a two-dimensional array.')
        return False
    axesList = []
    # Make a single list of plots to be plotted left -> right, then top -> bottom
    for i in range(rows):
        for j in range(cols):
            axesList.append(axes[i][j])
    if len(axesList) == 0:
        print('Error: no plot data available; plotting skipped.')
        return False
    # Define the matplotlib figure object
    fig = plt.figure(figsize = (self.axisWidth*cols, rows*self.axisHeight))
    # Create the axes with their plots
    for i in range(len(axesList)):
        if axesList[i] != "":
            ax = fig.add_subplot(rows, cols, i + 1, polar = axesList[i].polar)
            if axesList[i].xLabel:
                try:
                    ax.set_xlabel(axesList[i].xLabel)
                except:
                    pass
            if axesList[i].yLabel:
                try:
                    ax.set_ylabel(axesList[i].yLabel)
                except:
                    pass
            if axesList[i].title:
                try:
                    ax.set_title(axesList[i].title)
                except:
                    pass
            if axesList[i].xScale:
                try:
                        ax.set_xscale(axesList[i].xScale)
                except:
                    pass
            if axesList[i].yScale:
                try:
                        ax.set_yscale(axesList[i].yScale)
                except:
                    pass
            if len(axesList[i].xLim) == 2:
                try:
                    ax.set_xlim(axesList[i].xLim[0], axesList[i].xLim[1])
                except:
                    pass
            if len(axesList[i].yLim) == 2:
                try:
                    ax.set_ylim(axesList[i].yLim[0], axesList[i].yLim[1])
                except:
                    pass
            if len(axesList[i].traces) == 0:
                print('Error: Missing trace data for plotting!')
                return False

            for j in range(len(axesList[i].traces)):
                if axesList[i].traces[j].color:
                    Color = axesList[i].traces[j].color
                else:
                    Color = ini.defaultColors[j % len(ini.defaultColors)]
                if axesList[i].traces[j].marker:
                    Marker = axesList[i].traces[j].marker
                else:
                    Marker = ini.defaultMarkers[j % len(ini.defaultMarkers)]
                if axesList[i].traces[j].markerColor:
                    MarkerColor = axesList[i].traces[j].markerColor
                else:
                    MarkerColor = ini.defaultColors[j % len(ini.defaultColors)]
                try:
                    if axesList[i].xScaleFactor in list(SCALEFACTORS.keys()):
                        scaleX = 10**eval(SCALEFACTORS[axesList[i].xScaleFactor])
                    else:
                        scaleX = 1
                    if axesList[i].yScaleFactor in list(SCALEFACTORS.keys()):
                        scaleY = 10**eval(SCALEFACTORS[axesList[i].yScaleFactor])
                    else:
                        scaleY = 1
                    plt.plot(axesList[i].traces[j].xData/scaleX, axesList[i].traces[j].yData/scaleY, label = axesList[i].traces[j].label, linewidth = axesList[i].traces[j].lineWidth,
                                color = Color, marker = Marker, markeredgecolor = MarkerColor, markersize = axesList[i].traces[j].markerSize, markeredgewidth = 2, markerfacecolor = axesList[i].traces[j].markerFaceColor, linestyle = axesList[i].traces[j].lineType)
                except:
                    print("Error in plot data of '{0}'.".format(self.fileName))
                if axesList[i].text:
                    X, Y, txt = axesList[i].text
                    plt.text(X, Y, txt, fontsize = ini.plotFontSize)
                # Set default font sizes and grid
                defaultsPlot()
    # Save the figure"

    #Add 45 degrees lines to the plot!
    lineUp = patches.Arrow(0,0,-10e9,10e9,linewidth=3, edgecolor='r')
    lineDown = patches.Arrow(0,0,-10e9,-10e9,linewidth=3, edgecolor='r')
    ax.add_patch(lineUp)
    ax.add_patch(lineDown)

    plt.savefig(ini.imgPath + '45deg' + self.fileName)
    if self.show:
        plt.show()
    plt.close(fig)

    #Display it in the HTML file immediately :)
    img2html('45deg' + self.fileName, 400)
    return