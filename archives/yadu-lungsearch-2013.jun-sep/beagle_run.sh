#!/bin/bash
# IMPORTANT: Run this script only on beagle. This is not for running remotely from midway onto beagle

module load swift
clear;
set -x

echo "Initiating egsearch.swift run on beagle"
swift -tc.file tc.data -config beagle.cf -sites.file beagle_local.xml -cdm.file beagle.cdm egsearch.swift -lastSlice=10

