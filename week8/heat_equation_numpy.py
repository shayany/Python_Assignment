# -*- coding: utf-8 -*-
import time 
from matplotlib import pyplot 
from numpy import *
def solver_numpy(n=50,m=100,t0=0,t1=1000,dt=.1,nu=1):
    
    u=array(zeros((m,n),dtype='float'))
    f=array(ones((m,n),dtype='float'))
    pyplot.subplot(1,2,1)
    pyplot.imshow(u)
    loopCounter=t0
    #TIME
    tt1=time.time()
    #TIME
    firstRow=1
    firstCol=1
    lastRow=m-1       
    lastCol=n-1
    while(loopCounter<t1):
        u[firstRow:lastRow,firstCol:lastCol]=u[firstRow:lastRow,firstCol:lastCol] + dt \
                                            * (nu*u[firstRow-1:lastRow-1,firstCol:lastCol] \
                                            + nu*u[firstRow:lastRow,firstCol-1:lastCol-1] \
                                            - 4*nu*u[firstRow:lastRow,firstCol:lastCol] \
                                            + nu*u[firstRow:lastRow,firstCol+1:lastCol+1] \
                                            + nu*u[firstRow+1:lastRow+1,firstCol:lastCol] \
                                            + f[firstRow:lastRow,firstCol:lastCol])                 
        loopCounter+=dt
    #TIME
    tt2=time.time()
    print tt2-tt1
    #TIME
    pyplot.subplot(1,2,2)
    pyplot.imshow(u)
    pyplot.colorbar()
    pyplot.show()
    return u