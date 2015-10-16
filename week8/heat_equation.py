from matplotlib import pyplot 
def solver(n=50,m=100,u=0,t0=0,t1=10,dt=0.1,nu=1):

    u=[[0 for x in range(n)]for x in range(m)]
    f=[[1 for x in range(n)]for x in range(m)]
    pyplot.subplot(1,3,1)
    pyplot.imshow(u)
    loopCounter=t0
    pyplot.imshow(u,label="T0")
    while(loopCounter<t1):
        for i in range(1,m-1):
            for j in range(1,n-1):
                u[i][j]=u[i][j] + dt * (nu*u[i-1][j] + nu*u[i][j-1] - 4*nu*u[i][j] + nu*u[i][j+1] + nu*u[i+1][j] + f[i][j])
        loopCounter+=0.1
    pyplot.subplot(1,3,2)
    pyplot.imshow(u)
    pyplot.subplot(1,3,3)
    pyplot.colorbar()
    pyplot.show()
solver()
