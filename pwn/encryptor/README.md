# encryptor
pwn, easy〜medium

## テーマ
argv[0] leakの応用

## 脆弱性
Stack Overflow

## 解答までの流れ
1. ソースコードを読んで脆弱性に気づく
2. 脆弱性を使ってメモリリークする方法を考える
3. 秘密鍵をリークする
4. 暗号文を復号する

## 参考資料
[\_getopt\_internal\_r](https://code.woboq.org/userspace/glibc/posix/getopt.c.html#_getopt_internal_r)
[argp-parse.c](https://code.woboq.org/userspace/glibc/argp/argp-parse.c.html)
[argp-help.c](https://code.woboq.org/userspace/glibc/argp/argp-help.c.html)

## 問題文
Encryption only.
```
$ nc pwn-inu.chal.seccon.jp 9022
```

## FLAG
`SECCON{argv0-l34k_15_bur13d_1n_0bl1v10n??}`

## 確認して欲しい点

- [x] ROPなどの非想定解がない
- [x] `secret.key`の内容を知らずに復号できない
- [x] `secret.key`等、必要なファイルの内容を書き換えられない
- [x] `/tmp`等のディレクトリでlsできない（他人のソルバが見えない）

## 修正したい点

- [x] wallを禁止する
- [x] `echo hoge > /dev/pts/X` を禁止する
- [x] 他人のbashのkillを禁止する
- [ ] 定期的に初期化したい
