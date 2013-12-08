#!/bin/bash

clear;
set -x
export GLOBUS_HOSTNAME="swift.rcc.uchicago.edu"

#echo "Initiating egsearch.swift run on midway"
#swift -tc.file tc.data -sites.file midway.xml egsearch.swift -lastSlice=10

echo "Initiating egsearch.swift remote run on beagle"
swift -tc.file tc.data -config beagle.cf -sites.file beagle.xml egsearch.swift -lastSlice=10
