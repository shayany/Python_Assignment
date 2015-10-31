from matplotlib import pyplot 
import time 
from numpy import *
import numpy as np
cimport numpy as np
def solver_cython(np.ndarray[double, ndim=2] u_,np.ndarray[double, ndim=2] f_,int n=50,int m=100,double t0=0,double t1=1000,double dt=.1,double nu=1):
    """
    This function solve the heat equation 
    
    Parameteres:
    ------------
        u: initial distribution list (M*N)
        f: Heat source function list(M*N)
        t0: Start time
        t1: End time
        dt: Time step
        nu: Thermal diffusivity 
    Return:
    ------
        u: Updated u
    """      
    cdef int i
    cdef int j
    cdef double loopCounter=t0
    
    #cdef np.ndarray[double, ndim=1] u=1*u_
    #cdef np.ndarray[double, ndim=1] u_new=1*u_
    #cdef np.ndarray[double, ndim=1] f=1*f_

    cdef np.ndarray[double, ndim=1] u=u_.ravel()
    cdef np.ndarray[double, ndim=1] u_new=1*u
    cdef np.ndarray[double, ndim=1] f=f_.ravel()
    
    while(loopCounter<=t1):
        for i in xrange(1,n-1):
            for j in xrange(1,m-1):
                u_new[i*m+j]=u[i*m+j] + dt * (nu*u[(i-1)*m+j] + nu*u[i*m+j-1] - 4*nu*u[i*m+j] + nu*u[i*m+j+1] + nu*u[(i+1)*m+j] + f[i*m+j]);
        loopCounter+=dt
        #for i in xrange(0,n):
        #    for j in xrange(0,m):
        #       u[i*m + j]=u_new[i*m + j];
        u=1*u_new
    return u.reshape(n,m)
