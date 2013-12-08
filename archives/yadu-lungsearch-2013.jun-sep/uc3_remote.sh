#!/bin/bash
module load swift;
clear;
set -x
export GLOBUS_HOSTNAME="swift.rcc.uchicago.edu"

#echo "Initiating egsearch.swift remote run on UC3 WITHOUT CDM"
#swift -tc.file tc.data -config uc3.cf -sites.file uc3.xml egsearch.swift -lastSlice=50

echo "Initiating egsearch.swift remote run on UC3 WITH CDM"
time swift -tc.file tc.data -config uc3.cf -sites.file uc3.xml -cdm.file uc3.cdm egsearch.swift -lastSlice=1
