from numpy import *
from instant import inline_with_numpy
from matplotlib import pyplot
import time  
def solver_instant(n=50,m=100,t0=0,t1=1000,dt=.1,nu=1):
    c_code = """
double swap (int x1, int y1, double* u,int x2, int y2, double* f,int x3,double* args){
        double t0=args[0];
        double t1=args[1];
        double dt=args[2];
        double nu=args[3];
        double u_new[x1*y1];
        double counterLoop=t0;
    

        for (int i=0; i<x1; i++)
            for (int j=0; j<y1; j++)
                u_new[i*y1 + j]=u[i*y1 + j];
    
        while(counterLoop<t1)
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
    sum_func = inline_with_numpy(c_code, arrays = [['x1', 'y1', 'u'],
                                                   ['x2', 'y2', 'f'],
                                                   ['x3','args']],
                                cache_dir="_cache")

    u=array(zeros((m,n),dtype='double'))
    f=array(ones((m,n),dtype='double'))

    params=ones(4)
    params[0]=t0
    params[1]=t1
    params[2]=dt
    params[3]=nu

    pyplot.subplot(1,2,1)
    pyplot.imshow(u)
    #TIME
    tt1=time.time()
    #TIME
    sum_func(u,f,params)
    #TIME
    tt2=time.time()
    print tt2-tt1
    #TIME  
    pyplot.subplot(1,2,2)
    pyplot.imshow(u)
    pyplot.colorbar()
    pyplot.show()
    return u