#!/bin/bash

# Fill in the usernames below to customize swift config for user
BEAGLE_USERNAME=""
MIDWAY_USERNAME=""
UC3_USERNAME=""

if [[ -z $BEAGLE_USERNAME ]] 
then
    echo "Beagle username not provided. Skipping beagle configs"
else
    echo "rule .*csv DIRECT /lustre/beagle/$BEAGLE_USERNAME/"   > beagle.cdm
    cat beagle_local.xml | sed "s/{env.USER}/$BEAGLE_USERNAME/" > tmp && mv tmp beagle_local.xml
    cat beagle.xml       | sed "s/{env.USER}/$BEAGLE_USERNAME/" > tmp && mv tmp beagle.xml
    scp *.csv $BEAGLE_USERNAME@login.beagle.ci.uchicago.edu:/lustre/beagle/$BEAGLE_USERNAME/    
fi


if [[ -z $MIDWAY_USERNAME ]] 
then
    echo "Midway username not provided. Skipping midway configs"
else
    echo "rule .*csv DIRECT /scratch/midway/$MIDWAY_USERNAME/swiftwork" > midway.cdm
    cat midway.xml       | sed "s/{env.USER}/$MIDWAY_USERNAME/"         > tmp && mv tmp midway.xml
    scp *.csv $MIDWAY_USERNAME@swift.rcc.uchicago.edu:/scratch/midway/$MIDWAY_USERNAME/swiftwork/
fi

if [[ -z $UC3_USERNAME ]]
then
    echo "UC3 username not provided.    Skipping UC3 configs"
else
    echo "rule s\..*\.csv DEFAULT"                            > uc3.cdm
    echo "rule .*csv DIRECT /mnt/hadoop/$UC3_USERNAME/"      >> uc3.cdm
    cat uc3.xml          | sed "s/{env.USER}/$UC3_USERNAME/"  > tmp && mv tmp uc3.xml
    scp *.csv $UC3_USERNAME@uc3-sub.uchicago.edu:/mnt/hadoop/$UC3_USERNAME
fi
