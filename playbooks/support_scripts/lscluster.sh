#!/bin/ksh
lslpp -l cluster.es.server.rte >> /dev/null 2>&1
if [[ $? -eq 0 ]]; then
    cluster_name=$(/usr/es/sbin/cluster/utilities/cltopinfo -c | awk '/Cluster Name:/ {print $3}')
    echo "cluster_name=${cluster_name}"
    echo "halevel=$(/usr/es/sbin/cluster/utilities/halevel -s)"
    ipaddresses=$(/usr/es/sbin/cluster/utilities/cllsif | grep " service " | awk '{print $7}' | sort -u | tr "\n" " ")
    echo "ipaddresses=${ipaddresses}"
    start_scripts=$(/usr/es/sbin/cluster/utilities/cllsserv -c | cut -d':' -f1,2 | tr "\n" "@" | sed 's/@/, /g' | sed 's/, $//')
    echo "start_scripts=${start_scripts}"
    stop_scripts=$(/usr/es/sbin/cluster/utilities/cllsserv -c | cut -d':' -f1,3 | tr "\n" "@" | sed 's/@/, /g' | sed 's/, $//')
    echo "stop_scripts=${stop_scripts}"
    script_mode=$(/usr/es/sbin/cluster/utilities/cllsserv -c | cut -d':' -f1,4 | tr "\n" "@" | sed 's/@/, /g' | sed 's/, $//')
    echo "script_mode=${script_mode}"

    /usr/es/sbin/cluster/utilities/cltopinfo | awk '{
        if (/Cluster Type:/) {cluster_type=$3}
        else if (/Heartbeat Type:/) {
            heartbeat_type=$3
        }
        else if (/^NODE /) {
            gsub(":", "")
            cluster_nodes=cluster_nodes", "$2
        }
        else if (/Resource Group/) {
            rg=$3
            resource_groups=resource_groups", "rg
        }
        else if (/Startup Policy/) {
            txt=""
            for (i=3; i<=NF; ++i) {
                txt=txt" "$i
            }
            startup_policy=startup_policy", "rg":"txt
        }
        else if (/Fallover Policy/) {
            txt=""
            for (i=3; i<=NF; ++i) {
                txt=txt" "$i
            }
            fallover_policy=fallover_policy", "rg":"txt
        }
        else if (/Fallback Policy/) {
            txt=""
            for (i=3; i<=NF; ++i) {
                txt=txt" "$i
            }
            fallback_policy=fallback_policy", "rg":"txt
        }
    } END {
        print "cluster_nodes="cluster_nodes
        print "cluster_type="cluster_type
        print "heartbeat_type="heartbeat_type
        print "resource_groups="resource_groups
        print "startup_policy="startup_policy
        print "fallover_policy="fallover_policy
        print "fallback_policy="fallback_policy
    }' | sed 's/=, /=/g'

    /usr/es/sbin/cluster/utilities/cllsres | awk -F'=' '{
        if ($1 == "SERVICE_LABEL") {service_labels=$2}
        if ($1 == "APPLICATIONS") {applications=$2}
        if ($1 == "VOLUME_GROUP") {volume_groups=$2}
        if ($1 == "FS_BEFORE_IPADDR") {fs_before_ip=$2}
        if ($1 == "USERDEFINED_RESOURCES") {user_define_res=$2}
    }
    END {
        print "service_labels="service_labels;
        print "applications="applications;
        print "volume_groups="volume_groups;
        print "fs_before_ip="fs_before_ip;
        print "user_defined_res="user_define_res;
    }' | sed 's/""/NONE/g' | sed 's/"//g'
else
    echo "cluster_name=No_Cluster"
    echo "halevel=N/A"
    echo "cluster_type=N/A"
    echo "heartbeat_type=N/A"
    echo "cluster_nodes=N/A"
    echo "ipaddresses=N/A"
    echo "service_labels=N/A"
    echo "resource_groups=N/A"
    echo "start_scripts=N/A"
    echo "stop_scripts=N/A"
    echo "script_mode=N/A"
    echo "startup_policy=N/A"
    echo "fallover_policy=N/A"
    echo "fallback_policy=N/A"
    echo "applications=N/A"
    echo "volume_groups=N/A"
    echo "fs_before_ip=N/A"
    echo "user_defined_res=N/A"
fi
