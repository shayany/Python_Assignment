# -*- coding: utf-8 -*-
from numpy import *
def solver_numpy(u,f,n=100,m=50,t0=0,t1=1000,dt=.1,nu=1):
    """
    This function solve the heat equation 
    
    Parameteres:
    ------------
        u: initial distribution numpy array (M*N)
        f: Heat source function numpy array (M*N)
        t0: Start time
        t1: End time
        dt: Time step
        nu: Thermal diffusivity 
    Return:
    ------
        u: Updated u
    """    

    loopCounter=t0

    firstRow=1
    firstCol=1
    lastRow=n-1       
    lastCol=m-1
    while(loopCounter<=t1):
        u[firstRow:lastRow,firstCol:lastCol]=u[firstRow:lastRow,firstCol:lastCol] + dt \
                                            * (nu*u[firstRow-1:lastRow-1,firstCol:lastCol] \
                                            + nu*u[firstRow:lastRow,firstCol-1:lastCol-1] \
                                            - 4*nu*u[firstRow:lastRow,firstCol:lastCol] \
                                            + nu*u[firstRow:lastRow,firstCol+1:lastCol+1] \
                                            + nu*u[firstRow+1:lastRow+1,firstCol:lastCol] \
                                            + f[firstRow:lastRow,firstCol:lastCol])                 
                       
        loopCounter+=dt

    return u
