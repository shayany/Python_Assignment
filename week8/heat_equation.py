from matplotlib import pyplot 
import time 
import math
def solver(n=50,m=100,t0=0,t1=1000,dt=.1,nu=1):
    u=[[0.0 for x in range(n)]for x in range(m)]
    f=[[1.0 for x in range(n)]for x in range(m)]
    u_new=[[u[i][j] for j in range(n)]for i in range(m)]
    pyplot.subplot(1,2,1)
    pyplot.imshow(u)
    loopCounter=t0
    #TIME
    #tt1=time.time()
    #TIME
    while(loopCounter<t1):
        for i in xrange(1,m-1):
            for j in xrange(1,n-1):
                u_new[i][j]=u[i][j] + dt * (nu*u[i-1][j] + nu*u[i][j-1] - 4*nu*u[i][j] + nu*u[i][j+1] + nu*u[i+1][j] + f[i][j])
        loopCounter+=dt
        u=[[u_new[i][j] for j in range(n)]for i in range(m)]
    #TIME
    #tt2=time.time()
    #print tt2-tt1
    #TIME    
    pyplot.subplot(1,2,2)
    pyplot.imshow(u)
    pyplot.colorbar()
    pyplot.show()
    return u
    