#! /usr/bin/python

__author__ = "Grant Olsen"
__copyright__ = "Copyright 2017, Grant Olsen"

__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Grant Olsen"
__email__ = "jython.scripts@gmail.com"
__status__ = "Beta"

#--------------------------------#
# Advanced plot viewer for visualizing Unity script variables in realtime.
# Has added button that allows changing the style to a multi plot view.
#--------------------------------#

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button

class UPyPlot ():

    def __init__(self):
        self.fig = plt.figure("UPyPlot Advanced Window")
        self.fig.set_facecolor((0.63, 0.63, 0.63))

        self.ax = self.fig.add_subplot(1,1,1)
        self.ax.set_facecolor((0.87, 0.87, 0.87))
        self.axs = [self.ax]

        self.plotCombined = True
        axBtn = plt.axes([0, 0, 0.2, 0.07])
        self.bCombined = Button(axBtn, 'Style') #use "self" keyword to keep a reference
        self.bCombined.on_clicked(self.click)

    def run(self):
        ani = animation.FuncAnimation(self.fig, self.animate, interval=100)
        plt.show()

    def click(self, event):
        self.plotCombined = not self.plotCombined

    def manageAxes (self):
        def clearAllAxes():
            for i, ax in enumerate(self.axs):
                ax.remove()
            self.axs = []
        def createNewAxes(size, pos):
            ax = self.fig.add_subplot(size, 1, pos, zorder=-1) #zorder so the button is always in front
            ax.set_facecolor((0.87, 0.87, 0.87))
            return ax
        if self.plotCombined and self.axs.__len__() > 1:
            clearAllAxes()
            self.axs.append(createNewAxes(1, 1))
        elif not self.plotCombined and self.yElements.__len__() != self.axs.__len__():
            clearAllAxes()
            size = self.yElements.__len__()
            for n in xrange(1, size + 1):
                self.axs.append(createNewAxes(size, n))
        else:
            for ax in self.axs:
                ax.clear()

    def animate(self, i):
        try: #try to read in the file, if No such file or directory then just return and try again
            pollData = open("plotting_cache\plot.txt","r").read()
        except IOError:
            return

        try: #try to unpack the data in the file, if for any reason it fails then just drop everything and return to start a new cycle.
            dataArray = pollData.split('\n')[2:]
            dataHeader = pollData.split('\n')[1].split(',')
            dataMeta = pollData.split('\n')[0].split(',')
        except:
            return

        try: #try to cast the strings to numeric representaton, if there was a value error then just drop everything and return to start a new cycle.
            currentSample = int(dataMeta[0])
            gameTime = float(dataMeta[1])
        except ValueError:
            return

        self.nElements = dataHeader.__len__()
        self.yElements = [np.array([]) for x in xrange(self.nElements)]


        for i, eachLine in enumerate(dataArray):
            if len(eachLine) > 1:
                for n, val in enumerate(eachLine.split(',')):
                    self.yElements[n] = np.append(self.yElements[n], val)

        xar = np.linspace(gameTime - (i * 0.1), gameTime, i)
        if xar.shape[0] == currentSample:
            self.manageAxes()

            for n, yax in enumerate(self.yElements):
                if (yax.shape[0]==currentSample):
                    try: # try to display this axis, if the data is corrupt then just skip it this frame.
                        ax = self.axs[0 if self.plotCombined else n]
                        ax.plot(xar, yax, label=dataHeader[n])
                        ax.legend(loc='upper left', fontsize=7)
                    except:
                        pass

t = UPyPlot()
t.run()
