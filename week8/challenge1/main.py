from heat_equation_instant import solver_instant

from numpy import *
from plot import ShowPlot
row=100
col=200


u_numpy=array(zeros((col,row),dtype='double'))
f_numpy=array(ones((col,row),dtype='double'))

#ShowPlot(u_numpy)
%timeit Instant_result=solver_instant(u_numpy,f_numpy,col,row,t0=0,t1=5000,dt=.1,nu=1)
#ShowPlot(Numpy_result)

