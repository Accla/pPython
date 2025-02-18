#!/bin/bash

for mydir in `find . -maxdepth 1 -type d`; 
do 
    if [[ "$mydir" != "." ]]; then 
        echo "$mydir"; 
	pushd $mydir
	echo " "
	echo "Current working directory: `pwd`"
	echo " "
	MYSCR=`find . -name "exec*.sh"`
	# echo "Run script: $MYSCR"
	# $MYSCR
	echo " "
	echo "*************************"
	for mf in $MYSCR; 
	do 
	   echo Executing $mf . . . ; 
           ./$mf;
        done
	popd
    fi; 
done

