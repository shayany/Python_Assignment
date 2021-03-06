def solver(u,f,n=50,m=100,t0=0,t1=1000,dt=.1,nu=1):
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
    
    u_new=[[u[i][j] for j in range(m)]for i in range(n)]
    loopCounter=t0
    while(loopCounter<=t1):
        for i in xrange(1,n-1):
            for j in xrange(1,m-1):
                u_new[i][j]=u[i][j] + dt * (nu*u[i-1][j] + nu*u[i][j-1] - 4*nu*u[i][j] + nu*u[i][j+1] + nu*u[i+1][j] + f[i][j])
        loopCounter+=dt
        u=[[u_new[i][j] for j in range(m)]for i in range(n)]

    return u
    