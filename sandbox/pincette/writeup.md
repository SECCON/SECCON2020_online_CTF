README.mdの解答までの流れを参照。
solverの使い方は以下の通り。
```sh
cd solver
docker-compose run --rm client [対象ホスト] [対象ポート]
```
環境変数として`SECCON_HOST`と`SECCON_PORT`が設定されている場合は、コマンドライン引数より優先される。
