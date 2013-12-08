#!/bin/bash
#IMPORTANT: This script is to be run locally on midway.
clear;
set -x
module load swift;

#export GLOBUS_HOSTNAME="swift.rcc.uchicago.edu"
#echo "Initiating egsearch.swift run on midway"
#swift -tc.file tc.data -config midway.cf -sites.file midway.xml egsearch.swift -lastSlice=1

#echo "Initiating egsearch.swift run on midway -- Sandybridge"
#swift -tc.file tc.data -config midway.cf -sites.file midway_sandyb.xml egsearch.swift -lastSlice=1

echo "Initiating egsearch.swift run on midway -- Sandybridge + Westmere"
swift -tc.file tc.data -config midway.cf -sites.file midway.xml -cdm.file midway.cdm egsearch.swift -lastSlice=5

