# encryptor writeup
## 調査
ソースコードを読むと、引数の処理中にStack Overflow脆弱性があることに気づく。
```cpp
  case 'i':
    /* get input filepath */
    strcpy(args->path_i, arg);
    break;

  case 'o':
    /* get output filepath */
    strcpy(args->path_o, arg);
    break;
```
SSPが有効なのでROPはできない。
```
$ checksec -f encryptor
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Partial RELRO   Canary found      NX enabled    No PIE          No RPATH   No RUNPATH   96 Symbols     Yes      4               8       encryptor
```

## 計画
不正な引数を渡すと次のようなメッセージが出る。
```
$ ./encryptor -x
./encryptor: invalid option -- 'x'
Try `encryptor --help' or `encryptor --usage' for more information.
```
[getopt](https://code.woboq.org/userspace/glibc/posix/getopt.c.html#_getopt_internal_r)のソースコードを読むと、これには`argv[0]`がそのまま使われていることが分かる。

したがって、スタックオーバーフローで`argv[0]`のポインタを書き換えて`secret`に向けた状態で不正な引数を渡すと、invalid optionのメッセージ中でメモリリークが発生する。

`-i`オプションの方の`strcpy`はFORTIFYがかかっているが、なにを判定したのか`-o`の方にgccはFORTIFYをかけなかったので、そちらを利用してオーバーフローできる。

## Exploit
`argv[0]`は6バイトのポインタだが、これを`secret`の3バイトのポインタに書き換える必要がある。
`strcpy`はNULL終端なので1度に上3バイトをNULLにできないので、同じオプションを繰り返し渡すことで、`strcpy`を使って1バイトずつNULLを書き込む。

