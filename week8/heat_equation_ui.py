import cPickle as pickle
import argparse
from numpy import *
from plot import ShowPlot
import os
from heat_equation import solver
from heat_equation_instant import solver_instant
from heat_equation_numpy import solver_numpy
from heat_equation_swig import solver_swig
from heatEquationCython import solver_cython
import timeit

def timefunc(function,u_list,f_list,col,row,t0,t1,dt,nu):
    """
    This function used as a wrapper for timeit
    
    Parameteres
    ___________
    function:name of the function which should be called
    u_list:
    f_list:
    col:
    row:
    t0:
    t1:
    dt:
    nu:
        
    Return:
    Best execution time
    
    NB:
    Be cautious ,It takes time more than 10 minutes to estimate the time for
    solver which implemented only with python
    """
    def wrap():
        function(u_list,f_list,col,row,t0,t1,dt,nu)
    t = timeit.Timer(wrap)
    return t.timeit(10)/10
    
def writeOnDisk(temperatureMatrix,fileName):
    """
    Write a solution on disk
    
    Parameters:
    ___________
    temperatureMatrix:Array that contain the solution
    fileName:name of file
    """
    solutionFile=open(fileName,"w") 
    pickle.dump(temperatureMatrix,solutionFile)
    solutionFile.close()
def loadFromDisk(fileName):
    """
    Read initial value from disk
    
    Parameters:
    ___________
    fileName:name of file

    Returns:
    ________
    2D List that contains the initial value
    """   
    if os.path.isfile(fileName):
        temperatureFile=open(fileName,"r") 
        temperatureArray=pickle.load(temperatureFile)
        temperatureFile.close() 
        return temperatureArray
        
def ShowUI():        
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", help="number of the rows(N)",type=int)
    parser.add_argument("--m", help="specify number of the coloumns(M)",type=int)
    parser.add_argument("--t0", help="specify the start-time",type=float)
    parser.add_argument("--t1", help="specify the end-time",type=float)
    parser.add_argument("--dt", help="specify the timestep",type=float)
    parser.add_argument("--f", help="specify the thermal diffusivity coefficient",type=float)
    parser.add_argument("--nu", help="specify the constant heat source",type=float)
    
    parser.add_argument("input", help="input file")
    parser.add_argument("output", help="output file")

    parser.add_argument("--plot", help="if you want to save the plot",action="store_true")
    
    parser.add_argument("--method", help="specify the mothod for solving the equation Python[1] Numpy[2] SWIG[3] Instant[4] Cython[5]",type=int)
    parser.add_argument("--verbosity", help="increase output verbosity")
    parser.add_argument("--timeit", help="Report timing",action="store_true")
    args = parser.parse_args()

    if args.t0:
        t0=args.t0
    else:
        t0=0
    if args.t1:
        t1=args.t1
    else:
        t1=1000
    if args.dt:
        dt=args.dt
    else:
        dt=.1
    if args.f:
        fValue=args.f
    else:
        fValue=1
    if args.nu:
        nu=args.nu
    else:
        nu=1
    if args.method==2 or args.method==3 or args.method==4 or args.method==5:      
        u_numpy=asarray(loadFromDisk(args.input))
        col=len(u_numpy)
        row=len(u_numpy[0])
        if args.n:
            row=args.n        
        if args.m:
            col=args.m
        u_numpy=u_numpy[0:col,0:row].copy()
        f_numpy=fValue*array(ones((col,row),dtype='double'))
    else:
        u_list=loadFromDisk(args.input)    
        col=len(u_list)
        row=len(u_list[0])
        if args.n:
            row=args.n        
        if args.m:
            col=args.m
            
        u_list=[[u_list[j][i] for i in range(row)]for j in range(col)]     
        f_list=[[fValue for x in range(row)]for x in range(col)]
 
    if args.method==2:#Numpy                        
        if args.timeit:
            print(timefunc(solver_numpy, u_numpy,f_numpy,col,row,t0,t1,dt,nu))
        else:
            ShowPlot(u_numpy,args.plot)
            Numpy_result=solver_numpy(u_numpy,f_numpy,col,row,t0,t1,dt,nu)         
            ShowPlot(Numpy_result,args.plot)
            writeOnDisk(Numpy_result.tolist(),args.output)
    elif args.method==3:#Swig
        if args.timeit:
            print(timefunc(solver_swig, u_numpy,f_numpy,col,row,t0,t1,dt,nu))
        else:
            ShowPlot(u_numpy,args.plot)
            Swig_result=solver_swig(u_numpy,f_numpy,col,row,t0,t1,dt,nu)
            ShowPlot(Swig_result,args.plot)
            writeOnDisk(Swig_result.tolist(),args.output)
    elif args.method==4:#instant
        if args.timeit:
            print(timefunc(solver_instant,u_numpy,f_numpy,col,row,t0,t1,dt,nu))
        else:        
            ShowPlot(u_numpy,args.plot)
            Instant_result=solver_instant(u_numpy,f_numpy,col,row,t0,t1,dt,nu)
            ShowPlot(Instant_result,args.plot)
            writeOnDisk(Instant_result.tolist(),args.output)
    elif args.method==5:#Cython
        if args.timeit:
            print(timefunc(solver_cython,u_numpy,f_numpy,col,row,t0,t1,dt,nu))
        else: 
            ShowPlot(u_numpy,args.plot)
            Cython_result=solver_cython(u_numpy,f_numpy,col,row,t0,t1,dt,nu)
            ShowPlot(Cython_result,args.plot)
            writeOnDisk(Cython_result.tolist(),args.output)
    else:#Plain Python
        if args.timeit:
            print(timefunc(solver,u_list,f_list,col,row,t0,t1,dt,nu))
        else: 
            ShowPlot(u_list,args.plot)
            plainPython_result=solver(u_list,f_list,col,row,t0,t1,dt,nu)
            ShowPlot(plainPython_result,args.plot)
            writeOnDisk(plainPython_result,args.output)        