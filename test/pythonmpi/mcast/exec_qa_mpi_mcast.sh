#!/bin/bash

source /etc/profile

export QA_CASE='qa_mpi_mcast'
export QA_PYFILE="${QA_CASE}.py"

# import functions
source ../qa_functions.sh

# run parallel pPython with single process
run_parallel_p1

# run parallel pPython with multiple processes
run_parallel_pn


