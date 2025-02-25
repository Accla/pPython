#!/bin/bash

source /etc/profile

export QA_CASE='test_res_map'
export QA_PYFILE="${QA_CASE}.py"

# import functions
source ../qa_functions.sh

# run serial pPython with single process
run_serial

# run parallel pPython with single process
run_parallel_p1

