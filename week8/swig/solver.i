/* solver.i */
%module solver

%{
        #define SWIG_FILE_WITH_INIT
        #include "solver.h"
%}

%include "numpy.i"

%init %{
        import_array();
%}

%apply (int DIM1, int DIM2, double *INPLACE_ARRAY2) {(int x1, int y1, double* u)}
%apply (int DIM1, int DIM2, double *IN_ARRAY2) {(int x2, int y2, double* f)}

%include "solver.h"
