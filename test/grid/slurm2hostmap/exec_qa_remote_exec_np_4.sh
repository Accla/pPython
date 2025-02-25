#!/bin/bash

export QA_CASE='test_slurm2hostmap'
export QA_PYFILE="${QA_CASE}.py"

# import functions
source ../qa_functions.sh

# run parallel pPython with multiple processes
run_parallel_pn



