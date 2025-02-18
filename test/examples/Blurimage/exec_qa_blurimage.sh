#!/bin/bash

export QA_CASE='pBlurimage_book'
export QA_PYFILE="${QA_CASE}.py"

# import functions
source ../qa_functions.sh

# run serial pPython with single process
run_serial

# run parallel pPython with single process
export PPYTHON_LOCAL_FS='no'
run_parallel_p1

# run parallel pPython with multiple processes
export PPYTHON_LOCAL_FS='yes'
run_parallel_pn


