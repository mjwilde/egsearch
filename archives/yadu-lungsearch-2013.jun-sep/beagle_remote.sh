#!/bin/bash
# IMPORTANT: Run this script only on midway. This is for running remotely from midway onto beagle
# NOT tested on other hosts!
module load swift
clear;
set -x
export GLOBUS_HOSTNAME=swift.rcc.uchicago.edu
echo "Initiating egsearch.swift run on beagle"
swift -tc.file tc.data -config beagle.cf -sites.file beagle.xml -cdm.file beagle.cdm egsearch.swift -lastSlice=10


