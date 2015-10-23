Run this commands step by step in terminal:

First) swig -python -I.. solver.i (solver.py and solver.wrap.c will be created in the same directory)

Second) gcc -I.. -fPIC -I/usr/include/python2.7 -c test.c test_wrap.c -std=c99(solver.o and solver_wrap.o will be created in same the directory)

Third) gcc -shared -fPIC -o _solver.so solver.o solver_wrap.o
(_solver.so will be created)
