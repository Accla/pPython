"""pyMPI_COMM_WORLD - share MPI_COMM_WORLD among Python modules

    Import MPI_COMM_WORLD with Python pyMCW module
    (defined in PythonMPI.py and called in by MPI_Run())
    This is a work around to mimick MATLAB global variable, MPI_COMM_WORLD
    becauses Python global scope is not working consistently across multiple module files.
"""
# Define MPI_COMM_WORLD dictionary if not defined.
try: MPI_COMM_WORLD
except NameError: MPI_COMM_WORLD = None
if MPI_COMM_WORLD is None:
    MPI_COMM_WORLD = dict()
    MPI_COMM_WORLD['rank'] = 0
    MPI_COMM_WORLD['size'] = 1

########################################################
# PythonMPI
# Dr. Jeremy Kepner & Dr. Chansup Byun
# MIT Lincoln Laboratory
# kepner@ll.mit.edu & cbyun@ll.mit.edu
########################################################
# Copyright 2023 Massachusetts Institute of Technology
#
# Permission is herby granted, without payment, to copy, modify, display
# and distribute this software and its documentation, if any, for any
# purpose, provided that the above copyright notices and the following
# three paragraphs appear in all copies of this software.  Use of this
# software constitutes acceptance of these terms and conditions.
#
# IN NO EVENT SHALL MIT BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT,
# SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OF
# THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF MIT HAS BEEN ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# MIT SPECIFICALLY DISCLAIMS ANY EXPRESS OR IMPLIED WARRANTIES INCLUDING,
# BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT.
#
# THIS SOFTWARE IS PROVIDED "AS IS," MIT HAS NO OBLIGATION TO PROVIDE
# MAINTENANCE, SUPPORT, UPDATE, ENHANCEMENTS, OR MODIFICATIONS.
