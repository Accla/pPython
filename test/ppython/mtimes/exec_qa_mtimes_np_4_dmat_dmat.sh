#!/bin/bash

source /etc/profile

export QA_CASE='test_mtimes_dmat_dmat'
export QA_PYFILE="${QA_CASE}.py"

# import functions
source ../qa_functions.sh

# run parallel pPython with multiple processes
export NCASE=2
run_parallel_pn

