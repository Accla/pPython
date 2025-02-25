#!/bin/bash

export QA_CASE='test_remote_exec'
export QA_PYFILE="${QA_CASE}.py"

# import functions
source ../qa_functions.sh

# run parallel pPython with multiple processes
# need to enforce to be a batch job
export QA_BATCH='yes'
run_parallel_pn



