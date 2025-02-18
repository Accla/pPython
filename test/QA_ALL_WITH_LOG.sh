#!/bin/bash
# Main test script to drive the entire test cases

# Load anaconda module
soruce /etc/profile
module purge
module load anaconda/Python-ML-2025a


# Test types
# 1: QA tests on the development soruces
# 2: QA tests on a release candidate

QA_TYPE=1

# Defind which partition to use for the test
if [[ "x$GRID_QA_MACHINES"=="x" ]]; then
   # Not defined, set the default partition
   export GRID_QA_MACHINES='grid-xeon-p8'
fi

export QA_NPPN=1
export QA_BATCH=yes

if [[ $QA_TYPE -eq 1 ]] ; then
    # QA on the development source
    export PPYTHON_HOME=/home/gridsan/ch21778/devtools/git/pPython
    # Disable to use local filesystem for message kernel
    export PPYTHON_LOCAL_FS='no'

elif [[ $QA_TYPE -eq 2 ]] ; then
    #
    # QA on LLGrid beta release candidate
    #
    export PPYTHON_HOME=/home/gridsan/groups/llgrid_beta/pPython/v0.9.2
else
   echo "QA_TYPE is wrong. Exited."
   exit
fi

DATESTR=`date +%Y%m%d-%H%M%S`
./qa_all.sh |& tee qa_all.log-${DATESTR}
