from heat_equation import solver
from heat_equation_instant import solver_instant
from heat_equation_numpy import solver_numpy
from heat_equation_swig import solver_swig
from heatEquationCython import solver_cython
from numpy import *
from plot import ShowPlot
row=50
col=100

u_list=[[0.0 for x in range(row)]for x in range(col)]
f_list=[[1.0 for x in range(row)]for x in range(col)]
"""
#ShowPlot(u_list)
plainPython_result=solver(u_list,f_list,col,row,t0=0,t1=1000,dt=.1,nu=1)
#ShowPlot(plainPython_result)
"""
#ShowPlot(u_list)
Cython_result=solver_cython(u_list,f_list,col,row,t0=0,t1=1000,dt=.1,nu=1)
#ShowPlot(Cython_result)

u_numpy=array(zeros((col,row),dtype='double'))
f_numpy=array(ones((col,row),dtype='double'))
#ShowPlot(u_numpy)
Numpy_result=solver_numpy(u_numpy,f_numpy,col,row,t0=0,t1=1000,dt=.1,nu=1)
#ShowPlot(Numpy_result)

u_numpy=array(zeros((col,row),dtype='double'))
f_numpy=array(ones((col,row),dtype='double'))
#ShowPlot(u_numpy)
Swig_result=solver_swig(u_numpy,f_numpy,col,row,t0=0,t1=1000,dt=.1,nu=1)
#ShowPlot(Swig_result)

u_numpy=array(zeros((col,row),dtype='double'))
f_numpy=array(ones((col,row),dtype='double'))
#ShowPlot(u_numpy)
Instant_result=solver_instant(u_numpy,f_numpy,col,row,t0=0,t1=1000,dt=.1,nu=1)
#ShowPlot(Instant_result)