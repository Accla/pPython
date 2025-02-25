#!/bin/bash

export PPYTHON_LOCAL_FS=yes

export QA_CASE='qa_dmat_remap_case1'
export QA_PYFILE="${QA_CASE}.py"

# import functions
source ../qa_functions.sh

# run parallel pPython with multiple processes
run_parallel_pn





