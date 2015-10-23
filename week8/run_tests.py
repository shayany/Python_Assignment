from heat_equation_numpy import solver_numpy
from numpy import array,zeros,ones,pi,sin
from matplotlib import pyplot

def test_solver():
    m=50
    n=100
    nu=1
    u_numpy=array(zeros((n,m),dtype='double'))
    f_numpy=array(zeros((n,m),dtype='double'))
    analytic_u=array(zeros((n,m),dtype='double'))
    for i in xrange(n-1):
        for j in xrange(m-1):
            #f[i][j]="{} {}".format(i-1,j-1)                
            #f_numpy[i][j] = nu*((2*pi/n)**2 + (2*pi/m)**2)*sin(2*pi/m*i)*sin(2*pi/n*j) 
            #analytic_u[i][j]=sin(2*pi/m*i)*sin(2*pi/n*j)
            f_numpy[i][j] = nu*((2*pi/(m-1))**2 + (2*pi/(n-1))**2)*sin(2*pi/(n-1)*i)*sin(2*pi/(m-1)*j)     
            analytic_u[i][j] = sin(2*pi/(n-1)*i)*sin(2*pi/(m-1)*j)
                          
    #pyplot.imshow(abs(analytic_u))
    #pyplot.colorbar()
    #pyplot.show()

    u=solver_numpy(u_numpy,f_numpy,n,m,t0=0,t1=1000,dt=.1,nu=1)
    err_small=(abs(u-analytic_u)).max()
    assert err_small<.0012
    #pyplot.imshow(abs(u-analytic_u))
    #pyplot.colorbar()
    #pyplot.show()
    
    m=100
    n=200
    u_numpy_bigger=array(zeros((n,m),dtype='double'))
    f_numpy_bigger=array(zeros((n,m),dtype='double'))
    analytic_u_bigger=array(zeros((n,m),dtype='double'))
    for i in xrange(n-1):
        for j in xrange(m-1):
            #f[i][j]="{} {}".format(i-1,j-1)                
            #f_numpy[i][j] = nu*((2*pi/n)**2 + (2*pi/m)**2)*sin(2*pi/m*i)*sin(2*pi/n*j) 
            #analytic_u[i][j]=sin(2*pi/m*i)*sin(2*pi/n*j)
            f_numpy_bigger[i][j] = nu*((2*pi/(m-1))**2 + (2*pi/(n-1))**2)*sin(2*pi/(n-1)*i)*sin(2*pi/(m-1)*j)     
            analytic_u_bigger[i][j] = sin(2*pi/(n-1)*i)*sin(2*pi/(m-1)*j)
                          
    #pyplot.imshow(abs(analytic_u))
    #pyplot.colorbar()
    #pyplot.show()

    u_bigger=solver_numpy(u_numpy_bigger,f_numpy_bigger,n,m,t0=0,t1=1000,dt=.1,nu=1)
    err_bigger=(abs(u_bigger-analytic_u_bigger)).max()
    assert err_bigger>err_small