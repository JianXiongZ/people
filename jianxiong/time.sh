#!/bin/bash
cd $1/
for IP in `ls | grep 192.168`
do
 cd ../$1/
 control=`cat $IP | grep '\[Elapsed\]' | awk '{print $3}'`
 echo $IP
 cd ../$2/
 for miner in `cat $IP | grep '\[MM \ID' | awk '{print $6}' | sed 's/[^0-9]//g'`
    do
	   min=`echo "scale=1; $(($control-$miner)) / 60" | bc`
	   echo $min 
    done
 echo "positive number stand for controler starting before miner"
done
