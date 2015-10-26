from matplotlib import pyplot
from numpy import *
import time
def ShowPlot(u,saveFile=False):
    if saveFile:
        fig=pyplot.figure()
    pyplot.imshow(u)
    pyplot.colorbar()
    pyplot.show()
    if saveFile:
        fig.savefig(str(time.time())+".png")