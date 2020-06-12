#!/bin/bash
INPUT=$1
OLDIFS=$IFS
IFS=','
[ ! -f $INPUT ] && { echo "$INPUT file not found"; exit 99; }
while read a b noise v0 T delta s0 expNum 
do      
        echo  "==================================================="
        echo " Simulation: $expNum "
        echo  " IDM Parameters"
	echo -e "\tAcceleration : $a"
	echo -e "\tDeceleration : $b"
	echo -e "\tNoise : $noise"
	echo -e "\tDesirable Velocity : $v0"
	echo -e "\tSafe Time Headway : $T"
	echo -e "\tAcceleration exponent : $delta"
	echo -e "\tLinear Jam Distance : $s0"
        echo " Starting simulation with the given parameters ... "
        p3 straight_road_test.py $a $b $noise $v0 $T $delta $s0 
        echo " Simulation complete!"
        echo "==================================================="
	echo ""
done < $INPUT
IFS=$OLDIFS

#need to read data from shell script to python sim
#need to typecast in python
#need to create python file that creates these parameters
