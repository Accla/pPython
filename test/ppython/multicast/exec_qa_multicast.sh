#!/bin/bash

source /etc/profile

export QA_CASE='test_multicast'
export QA_PYFILE="${QA_CASE}.py"

# import functions
source ../qa_functions.sh

# run parallel pPython with multiple processes
run_parallel_pn

