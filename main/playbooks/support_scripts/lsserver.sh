#!/bin/ksh
lparstat -i | egrep "^Node Name |^Partition Number |^Type   |^Mode      |^Entitled Capacity   |^Online Memory   |^Online Virtu
al CPUs  " | awk -F":" '{sub(/[ ,]+$/,"",$1); print $1"="$2}' | sed 's/= /=/g'
echo "Oslevel=$(oslevel -s)"
lslpp -l cluster.es.server.rte >> /dev/null 2>&1
if [[ $? -eq 0 ]]; then
   cluster_name=$(/usr/es/sbin/cluster/utilities/cltopinfo -c | awk '/Cluster Name:/ {print $3}')
   echo "Cluster Name=${cluster_name}"
else
   echo "Cluster Name=No_Cluster"
fi
ip=$(host $(hostname) | cut -d' ' -f3 | sed 's/,//g')
echo "IP Address=$ip"
