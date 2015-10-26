from matplotlib import pyplot 
import time 

"""def csum(list array):
  cdef int i, N=len(array)
  cdef double x, s=0.0
  for i in range(N):
      x = array[i]
      s += x
  return s"""
  

def solver_cython(list u,list f,int n=50,int m=100,float t0=0,float t1=1000,float dt=.1,float nu=1):
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
    cdef int I,J,M,N        
    cdef double U_NEW[500][500]
    cdef double U[500][500]
    cdef double F[500][500]
    cdef float T0,T1,DT,NU
    
    T0=t0
    T1=t1
    DT=dt
    NU=nu
    
    M=m
    N=n
    
    for I in range(N):
        for J in range(M):
            U[I][J]=u[I][J]
            U_NEW[I][J]=u[I][J] 
            F[I][J]=f[I][J]  
    #u_new=[[u[i][j] for j in range(m)]for i in range(n)]
    
    #pyplot.subplot(1,2,1)
    #pyplot.imshow(u)
    cdef float loopCounter=T0
    #TIME
    #tt1=time.time()
    #TIME
    while(loopCounter<T1):
        for I in range(1,N-1):
            for J in range(1,M-1):
                U_NEW[I][J]=U[I][J] + DT * (NU*U[I-1][J] + NU*U[I][J-1] - 4*NU*U[I][J] + NU*U[I][J+1] + NU*U[I+1][J] + F[I][J])
        for I in range(N):
            for J in range(M):
                U[I][J]=U_NEW[I][J]
        loopCounter+=DT
    #TIME
    #tt2=time.time()
    #print "Cython Time: {}s".format(tt2-tt1)
    #TIME 
    for I in range(N):
        for J in range(M):
                u[I][J]=U[I][J]   
    #pyplot.subplot(1,2,2)
    #pyplot.imshow(u)
    #pyplot.colorbar()
    #pyplot.show()
    return u
