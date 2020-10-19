# CONVaaS

logging.config でシェルを取る問題です。

## テーマ

JSON や YAML といったフォーマットを相互に変換できる TCP サービスがテーマです。

## 脆弱性

logging.config の dictConfig に渡るファイルの上書きです。

## 解答までの流れ

1. コードや Dockerfile を読んだり実際に動かしてみて logging.yaml が上書きできることに気づく。
2. logging.config のリファレンスを読んだりして、任意のクラスをインスタンス化できることに気づく。
3. logging.config を読んで exploit の YAML を書いて投げる。

## 参考資料

- https://docs.python.org/3/library/logging.config.html

## 問題文

Converter as a Service.

`nc {{SECCON_HOST}} {{SECCON_PORT}}`

## FLAG

`SECCON{c0nver7in9_lo9g1ng_c0nfi9_in7o_c0nven1en7_sh3l1}`
