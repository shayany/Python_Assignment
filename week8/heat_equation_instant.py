from numpy import *
from instant import inline_with_numpy
from matplotlib import pyplot
import time  
def solver_instant(u,f,n=50,m=100,t0=0,t1=1000,dt=.1,nu=1):
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
        
    c_code = """
double calculate (int x1, int y1, double* u,int x2, int y2, double* f,int x3,double* args){
        double t0=args[0];
        double t1=args[1];
        double dt=args[2];
        double nu=args[3];
        double u_new[x1*y1];
        double counterLoop=t0;
    

        for (int i=0; i<x1; i++)
            for (int j=0; j<y1; j++)
                u_new[i*y1 + j]=u[i*y1 + j];
    
        while(counterLoop<=t1)
        {
            for(int i=1;i<x1;i++)
            {
                for(int j=1;j<y1;j++)
                    u_new[i*y1+j]=u[i*y1+j] + dt * (nu*u[(i-1)*y1+j] + nu*u[i*y1+j-1] - 4*nu*u[i*y1+j] + nu*u[i*y1+j+1] + nu*u[(i+1)*y1+j] + f[i*y1+j]);
            }
            for (int i=1; i<x1-1; i++)
                for (int j=1; j<y1-1; j++)
                    u[i*y1 + j]=u_new[i*y1 + j];
            counterLoop+=dt;
        }    
}
"""
    call_func = inline_with_numpy(c_code, arrays = [['x1', 'y1', 'u'],
                                                   ['x2', 'y2', 'f'],
                                                   ['x3','args']],
                                cache_dir="_cache")


    params=ones(4)
    params[0]=t0
    params[1]=t1
    params[2]=dt
    params[3]=nu

    call_func(u,f,params)
 
    return u
