import time 
from matplotlib import pyplot 
from numpy import *
def solver_numpy(n=50,m=100,u=0,t0=0,t1=1000,dt=0.1,nu=1):
    
    u=zeros((m,n),dtype='float')
    f=ones((m,n),dtype='float')
    pyplot.subplot(1,2,1)
    pyplot.imshow(u)
    loopCounter=t0
    #tt1=time.time()
    while(loopCounter<t1):
        u[1:m-1,1:n-1]=u[1:m-1,1:n-1] + dt * (nu*u[0:m-2,1:n-1] + nu*u[1:m-1,0:n-2] - 4*nu*u[1:m-1,1:n-1] + nu*u[1:m-1,2:n] + nu*u[2:m,1:n-1] + f[1:m-1,1:n-1]) 
        loopCounter+=0.1
    #TIME
    #tt2=time.time()
    #print tt2-tt1
    #TIME
    pyplot.subplot(1,2,2)
    pyplot.imshow(u)
    pyplot.colorbar()
    pyplot.show()
