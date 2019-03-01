#!/bin/ksh
# Listing all RPM packages, and grepping specific fields
for rpm in $(rpm -qa | sort);
do
    rpm -qi ${rpm} | sed 's/ *: */:/g' | awk '{gsub(/   +/,"\n")}1' | \
    egrep -i "^Name:|^Version:|^Release:|^Size |^Build Date:|^Build Host:|^Relocations:|Install Date:|^License:" | \
    sed 's/:/=/1'
    echo "-NEXT-"
done
