from numpy import *
from swig.solver import calculate
def solver_swig(u,f,n=50,m=100,t0=0,t1=1000,dt=.1,nu=1):
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


    calculate(u,f,t0,t1,dt,nu)

    return u