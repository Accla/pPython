#!/bin/bash
#
# Script to launch pgStrea.py benchmark for either CPU or GPU 
# 
# Load the anaconda or conda module where pPython is installed with.
#
source /etc/profile
module load anaconda/Python-ML-2024b

# This allows to see the actual job submission command
export PPYTHON_DEBUG=YES
# Define the partition to submit the job
PARTITION='e9-h100nvl'
# pRuN() 3rd argument input
TARGET="'$PARTITION&'"

# In order to use GPU, export the following two environment variables
export GPU=1
export PPYTHON_GPU_BINDING=yes
# To run on CPUs, comment above two line and uncomment the following line
# export GPU=

if [[ "x$GPU" == "x" ]]; then
   # CPU job
   type_str="CPU"
else
   # GPU job
   type_str="GPU"
fi

for NPPN in 1 2 ; do
    # echo $NPPN
    if [ "$NPPN" -lt "4" ]; then
        export LOGN=30
        export NTRIALS=1000
    elif [ "$NPPN" -lt "32" ]; then
        export LOGN=30
        export NTRIALS=1000
    elif [ "$NPPN" -eq "32" ]; then
        export LOGN=30
        export NTRIALS=1000
    fi
    echo "NPPN = $NPPN; LOGN = $LOGN; NTRIALS = $NTRIALS"
    echo python -c "import pPython; from pRUN import pRUN; pRUN('pgStream.py',[1,$NPPN,1],$TARGET); exit()"
    python -c "import pPython; from pRUN import pRUN; pRUN('pgStream.py',[1,$NPPN,1],$TARGET); exit()"

    # Wait for the job to be completed
    sleep 1
    while true 
    do 
        STAT=`LLstat |grep pgStream`
        # echo $STAT
        if [[ "x$STAT" == "x" ]]; then
            break
        else
            echo "Waiting for 60 seconds . . ."
            sleep 60
        fi
    done
    #
    # Rename PythonMPI
    FNPPN=$(printf "%02d" "$NPPN")
    mv PythonMPI PythonMPI_$PARTITIION_${type_str}_${FNPPN}
done

