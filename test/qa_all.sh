#!/bin/bash

# List of directories by test cases
# MYDIRLIST="examples dmat dmap ppython pythonmpi"
MYDIRLIST="examples "

for mydir in $MYDIRLIST; 
do 
   cd $mydir
   echo "$mydir, ./run .. "
   ./run_all_dirs.sh
   cd ..
done
