void calculate(int x1, int y1, double* u,int x2,int y2, double* f,double t0,double t1,double dt,double nu){
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
