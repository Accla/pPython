#!/bin/bash


export QA_CASE='dmat_assign_cyclic_c3'
export QA_PYFILE="${QA_CASE}.py"
export QA_BATCH="yes"
export QA_NPPN=4

# import functions
source ../qa_functions.sh

# run serial pPython with single process
# run_serial

# run parallel pPython with single process
# run_parallel_p1

# run parallel pPython with multiple processes
run_parallel_pn


