# テーマ
 コマンドインジェクションを防ぐ用に設定したWAFを突破する

# 脆弱性
 コマンドインジェクション

# 問題文・ヒント
 flagを実行してみて!

 問題Webサーバと、以下を一緒に提供する
 
* index.cgi  # コマンドインジェクションの脆弱性があるcgi
* rules.conf # WAFの設定

# 解答までの流れ

1. コマンドインジェクションの脆弱性があるWebサーバを用意

2. WAFを回避しつつコマンドインジェクションしてもらう

攻撃者がよくやる /usr/bin/wget のコマンドインジェクションを模して/usr/bin/flagを実行してもらう

ただし、WAF(Apacheのmod_security)で怪しいリクエストを防ぐ
※mod_securityの定義は問題として提供する

```
  [リクエストのルール] ※ルールは難易度により調整
    × やたら長いリクエスト(320文字までに制限)
    × 数字が含まれている
    × u,s,r,b,i,n,f,l,a,g のいずれかが含まれている
    × U,S,R,B,I,N,F,L,A,G のいずれかが含まれている
    × 同じ英文字は2回使えない

  [レスポンスのルール]
    × SECCONが含まれている
```

# 参考資料

Bash $((算術式)) のすべて
https://qiita.com/akinomyoga/items/2dd3f341cf15dd9c330b