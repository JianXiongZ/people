#!/bin/bash
# This a script for toohot statics
# Config ~/.my.cnf before use this script
IPLIST="(ip='10.13.16.2' or ip='10.13.47.1' or ip='10.13.47.2')"

getstats() {
        echo -n time:$1 $2/$3 $4,

        HOT_CNT=`mysql -N -B -A -e "select distinct dna from module where ${IPLIST} and ((ec>>1) & 1=1) and time > '$1 $2' and time < '$3 $4';" amsv3 | wc -l`
        TEMP=`mysql -N -B -A -e "select max(temp) from module where ${IPLIST} and time > '$1 $2' and time < '$3 $4';" amsv3`
        TEMP0=`mysql -N -B -A -e "select max(temp0) from module where ${IPLIST} and time > '$1 $2' and time < '$3 $4';" amsv3`
        TEMP1=`mysql -N -B -A -e "select max(temp1) from module where ${IPLIST} and time > '$1 $2' and time < '$3 $4';" amsv3`

        echo -n "hot count:${HOT_CNT},highest temp(CTRL):${TEMP},highest temp(Hashboard):"
        if [ ${TEMP0} > ${TEMP1} ]; then
                echo ${TEMP0}
        else
                echo ${TEMP1}
        fi
}

# run with 601601-5d8a1270
STARTTIME="2016-03-14 20:07:01"
ENDTIME="2016-03-16 01:09:00"
getstats ${STARTTIME} ${ENDTIME}

# Don't care controller board
STARTTIME="2016-03-16 18:25:00"
ENDTIME="2016-03-16 21:48:42"
getstats ${STARTTIME} ${ENDTIME}

# Increase the default temp
STARTTIME="2016-03-16 21:48:42"
ENDTIME="2016-03-16 23:59:59"
getstats ${STARTTIME} ${ENDTIME}

