#!/bin/bash

export QA_CASE='qa_dmat_fft'
export QA_PYFILE="${QA_CASE}.py"

# import functions
source ../qa_functions.sh

# run serial pPython with single process
run_serial

# run parallel pPython with single process
run_parallel_p1

# enforce mixed mode when using interactive triples mode
export PPYTHON_LOCAL_FS=yes

# run parallel pPython with multiple processes
run_parallel_pn


