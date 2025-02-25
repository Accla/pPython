#!/bin/bash

source /etc/profile

export QA_CASE='test_agg'
export QA_PYFILE="${QA_CASE}.py"

export PPYTHON_LOCAL_FS=yes
export QA_BATCH=no
export export QA_NPPN=2

# import functions
source ../qa_functions.sh

# run parallel pPython with multiple processes
run_parallel_pn

