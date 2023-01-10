#!/bin/bash

EXAMPLE_DIR="../examples"

echo " "
for mydir in `ls $EXAMPLE_DIR`; 
do echo $mydir; 
   PYFILE=`grep py_file $EXAMPLE_DIR/$mydir/RUN.py|grep '='|cut -d= -f2`; 
   PYFILE="${PYFILE:2:-1}"; 
   echo "My pPython file: $PYFILE"
   cp ./RUN.py $EXAMPLE_DIR/$mydir/RUN.py 
   sed -i s/param_sweep_parallel.py/$PYFILE/ $EXAMPLE_DIR/$mydir/RUN.py 
   echo " "
done


