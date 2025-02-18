#!/bin/bash

function wait_job() {
   # Argument $1 is the name of job
   running=1
   while [ $running -le 5 ]
   do
      sleep 10
      JOB=`LLstat | grep $1`
      echo "$JOB"
      if [[ "x$JOB" == "x" ]]; then
         running=10
         echo "Check if the job finished successfully."
         ERROR=`cat PythonMPI/*.err`
         if [[ "x$ERROR" == "x" ]]; then
            echo " "
            echo "SUCCESS "
            echo " "
         else
            echo " "
            echo "FAILED "
            echo "====== "
            echo "$ERROR"
            echo " "
         fi
      fi
      # running=$(($running+1))
   done
}

function run_serial() {
   
   # Run a single process (serial mode):
   echo " "
   echo " "
   echo "***> Run a single process (serial mode):"
   echo " "
   echo " "
   export QA_PARALLEL=0
   export QA_NPROCS=1
   export QA_MACHINES={}
   export PPYTHON_CLASSIC=1

   MODE="serial"
   python qa_run_on_llsc.py |& tee qa_${QA_CASE}_${MODE}_np_${QA_NPROCS}.log
   echo "... Completed serial mode run with 1 process"
}

function run_parallel_p1() {
   # Run a single process (parallel mode):
   echo " "
   echo " "
   echo " "
   echo "***> Run a single process (parallel mode):"
   echo " "
   echo " "
   echo " "
   export QA_PARALLEL=1
   export QA_NPROCS=1
   if [[ "$PPYTHON_LOCAL_FS" == "no" ]]; then
      #export QA_MACHINES='grid-xeon-e5'
      export QA_MACHINES=$GRID_QA_MACHINES
   else
      #export QA_MACHINES='grid-xeon-e5&'
      export QA_MACHINES="${GRID_QA_MACHINES}&"
   fi
   export PPYTHON_CLASSIC=1

   MODE="parallel"
   python qa_run_on_llsc.py |& tee qa_${QA_CASE}_${MODE}_np_${QA_NPROCS}.log
   if [[ "$PPYTHON_LOCAL_FS" == "no" ]]; then
      echo "... Completed parallel mode run with 1 process"
   else
      wait_job ${QA_PYFILE:0:12}
      if [[ "x$PPYTHON_CLASSIC" == "x" ]] ; then
         # Triples mode
         RN=`echo $QA_NPROCS \* 2  - 1|bc`
         NS=`grep SUCCESS PythonMPI/p*/*out| wc -l`
      else
         # Classic mode
         RN=`echo $QA_NPROCS`
         NS=`grep SUCCESS PythonMPI/*out| wc -l`
      fi
      echo "... Number of SUCCESS: $NS (should be $RN)"
   fi
}

function run_parallel_pn() {
   # Run multiple processes (parallel mode):
   echo " "
   echo " "
   echo "***> Run multiple processes (parallel mode):"
   echo " "
   echo " "
   export QA_PARALLEL=1
   export QA_NPROCS=4  # Np should be power of 2 number

   # Use triples mode job
   export PPYTHON_CLASSIC=

   if [[ "x$QA_BATCH" == "xyes" ]]; then
      export QA_MACHINES="${GRID_QA_MACHINES}&"
   else
      # export QA_MACHINES='grid-xeon-e5'
      export QA_MACHINES="${GRID_QA_MACHINES}"
      # enforce mixed filesystem for interactive tripes mode jobs
      export PPYTHON_LOCAL_FS=yes
   fi

   MODE="parallel"
   python qa_run_on_llsc.py |& tee qa_${QA_CASE}_${MODE}_np_${QA_NPROCS}.log

   #
   echo "Check the status of other parallel processes:"
   wait_job ${QA_PYFILE:0:12}
   if [[ "x$PPYTHON_CLASSIC" == "x1" ]] ; then
      RN=`echo $QA_NPROCS`
      NS=`grep SUCCESS PythonMPI/*out| wc -l`
   else
      if [[ "x$QA_BATCH" == "xyes" ]]; then
         RN=`echo $QA_NPROCS \* $QA_NPPN |bc`
         NS=`grep SUCCESS PythonMPI/p*/*out| wc -l`
      else
         RN=`echo $QA_NPROCS \* $QA_NPPN - 1 |bc`
         NS=`grep SUCCESS PythonMPI/p*/*out| wc -l`
      fi
   fi
   if [[ "x$NCASE" != "x" ]]; then
      RN=$(($RN*$NCASE))
      echo "... Number of SUCCESS: $NS (should be $RN)"
   else
      echo "... Number of SUCCESS: $NS (should be $RN)"
   fi
}

