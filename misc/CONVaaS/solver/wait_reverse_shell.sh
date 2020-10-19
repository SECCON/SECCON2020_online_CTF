#/bin/bash

set -e -x

container_name=$(docker container ls --filter=name=proxy --format='{{.Names}}')
default_network=$(docker container inspect --format='{{range $k, $v := .NetworkSettings.Networks}}{{if (eq (index (split $k "_") 1) "default")}}{{$k}}{{end}}{{end}}' "${container_name}")

if [ -z $2 ]
then
    lhost=$(docker container inspect --format='{{.NetworkSettings.Networks.'"${default_network}"'.Gateway}}' "${container_name}")
else
    lhost=$2
fi
lport=$1

set +x
stty raw -echo && exec socat tcp-listen:"${lport}",reuseaddr,fork,bind="${lhost}" file:"$(tty)",raw,unlink-close=0
