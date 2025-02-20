#!/bin/bash

source /etc/profile

export QA_CASE='test_agg'
export QA_PYFILE="${QA_CASE}.py"

export PPYTHON_LOCAL_FS=yes
export QA_BATCH=no

# import functions
source ../qa_functions.sh

# run parallel pPython with multiple processes
run_parallel_pn

