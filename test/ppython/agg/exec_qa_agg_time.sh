#!/bin/bash

source /etc/profile

export QA_CASE='test_agg_time'
export QA_PYFILE="${QA_CASE}.py"

export PPYTHON_LOCAL_FS=yes
export PPYTHON_DEBUG=1

export PPYTHON_CLASSIC=1

# import functions
source ../qa_functions.sh

# run parallel pPython with multiple processes
run_parallel_pn
