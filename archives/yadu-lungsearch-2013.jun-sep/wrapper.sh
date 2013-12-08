#!/bin/bash

set -x 

echo $HOSTNAME

if [ `echo $HOSTNAME | grep "uc3"` ]
then
# UC3 Specific setup
    echo "On UC3"
    export PYTHONPATH=/cvmfs/uc3.uchicago.edu/groups/swift/lib/python2.7
    export LD_LIBRARY_PATH=/cvmfs/uc3.uchicago.edu/groups/swift/lib:/cvmfs/uc3.uchicago.edu/groups/swift/lib64/atlas:/cvmfs/uc3.uchicago.edu/groups/swift/lib64
    export PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/root/bin:/cvmfs/uc3.uchicago.edu/groups/swift/bin/
    export PATH=/cvmfs/uc3.uchicago.edu/groups/swift/bin/:$PATH    
    ls -lah /mnt/hadoop/{env.USER}/*
    ls -lah /mnt/hadoop/$USER/*
#End UC3
elif [ `echo $HOSTNAME | grep "beagle"` ]
then
# Beagle specific setup
    echo "On Beagle"
    export PYTHONPATH=/soft/python/2.7/2.7.3-vanilla/modules/scikit-learn/0.14/lib/python2.7/site-packages:/soft/python/2.7/2.7.3-vanilla/modules/scipy/0.12.0/lib/python2.7/site-packages:/soft/python/2.7/2.7.3-vanilla/modules/numpy/1.7.0/lib/python2.7/site-packages:/soft/python/2.7/2.7.3-vanilla/modules/scikit-learn/0.14/lib/python2.7/site-packages:/soft/python/2.7/2.7.3-vanilla/modules/scipy/0.12.0/lib/python2.7/site-packages:/soft/python/2.7/2.7.3-vanilla/modules/numpy/1.7.0/lib/python2.7/site-packages:/soft/python/2.7/2.7.3-vanilla/modules
    export LD_LIBRARY_PATH=/soft/python/2.7/2.7.3-vanilla/python/lib:/opt/gcc/mpc/0.8.1/lib:/opt/gcc/mpfr/2.4.2/lib:/opt/gcc/gmp/4.3.2/lib:/opt/gcc/4.7.2/snos/lib64:/soft/torque/2.5.7/lib:/soft/ci/lib
    export PATH=/soft/python/2.7/2.7.3-vanilla/python/bin:/soft/python/2.7/2.7.3-vanilla/virtualenvs/ober/bin:$PATH
 #End Beagle
elif [ `echo $HOSTNAME | grep "midway"` ]
then
# Midway specific setup
    echo "On Midway : $HOSTNAME"
    module load python;
    # This is accessible to other users
    export PYTHONPATH=/home/yadunand/scratch-midway/scikit-learn
    export PYTHONPATH=$PYTHONPATH:/home/yadunand/python/scikit-learn
# End Midway
fi

# Python ENV tests
# which python;
# python -c "import sklearn";
# python -c "from sklearn.svm import SVC"

# Platform independant script 
echo "Checking for the input files ";
ls -lah;
echo "Python script to execute : $1"
echo "Executing.... python $1 $2 $3 $4"
python $1 $2 $3 $4

# Platform independent script ends