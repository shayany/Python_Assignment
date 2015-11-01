from matplotlib import pyplot
from numpy import *
import time
def ShowPlot(u,saveFile=False):
    if saveFile:
        fig=pyplot.figure()
    pyplot.imshow(u)
    if array(u).max()>0 :
        pyplot.colorbar()
    pyplot.show()
    if saveFile:
        fig.savefig(str(time.time())+".png")