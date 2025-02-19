#!/bin/bash


export PPYTHON_LOCAL_FS=yes

export QA_CASE='qa_dmat_agg_reconstruct_cyclic'
export QA_PYFILE="${QA_CASE}.py"
export QA_BATCH="yes"

# import functions
source ../qa_functions.sh

# run parallel pPython with multiple processes
run_parallel_pn



