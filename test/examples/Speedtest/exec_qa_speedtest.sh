#!/bin/bash

export QA_CASE='qa_speedtest'
export QA_PYFILE="${QA_CASE}.py"

# import functions
source ../qa_functions.sh

# run parallel pPython with single process
run_parallel_p1



