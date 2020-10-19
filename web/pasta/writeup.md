# 解法

## フラグの位置の特定

`service-a/main.go` を読むと、`docker-compose.yml` 中で定義されているサービス `service-a` に対し、`x-auth-role: admin` ヘッダを持ったリクエストを送ると、そのレスポンスとしてフラグが得られることがわかる。

## フラグに至る経路の考察

`service-a` に対してリクエストを送信し、そのレスポンスを得ることは、必ずサービス `nginx` を経由することになることが `nginx/conf/default.conf` と `docker-compose.yml` を読むとわかる。
とりわけ `nginx/conf/default.conf` に以下の箇所からは、以下のようなことがわかる。

1. `service-a` に対してリクエストを送信するためには、`auth_request` によりフォワードされた `http://auth/validate` へのリクエストに対し、2xx のレスポンスが得られている必要がある。
2. `x-auth-role` ヘッダは、`http://auth/validate` からのレスポンスに含まれる `x-auth-role` ヘッダの値にセットされる。

```nginx
location / {
    auth_request /proxy/validate;

    auth_request_set $x_auth_uid $upstream_http_x_auth_uid;
    proxy_set_header x-auth-uid $x_auth_uid;

    auth_request_set $x_auth_issuer $upstream_http_x_auth_issuer;
    proxy_set_header x-auth-issuer $x_auth_issuer;

    auth_request_set $x_auth_role $upstream_http_x_auth_role;
    proxy_set_header x-auth-role $x_auth_role;

    proxy_pass http://service-a/;
  }

/* ... 省略 ... */

  location = /proxy/validate {
    internal;
    proxy_pass http://auth/validate;
  }
```

ところで、エンドポイント `http://auth/validate` は、`auth/main.go` の以下のような処理に紐づいている。

```go
	http.HandleFunc("/validate", func(w http.ResponseWriter, r *http.Request) {
		log.Printf("validate: %v", r)

		authToken, ok := extractAuthToken(r.Cookies())
		if !ok {
			// there's no auth token in cookies.
			w.WriteHeader(http.StatusUnauthorized)
			return
		}

		token, err := jwt.Parse(authToken, generateKeySelector(publicKey))
		if err != nil {
			// auth token is weird.
			w.WriteHeader(http.StatusUnauthorized)
			return
		}

		if ok := validateTokenHeader(token, rootPool); !ok {
			// the header seems to be broken.
			w.WriteHeader(http.StatusForbidden)
			return
		}

		if !token.Valid {
			// the signature is broken.
			w.WriteHeader(http.StatusForbidden)
			return
		}

		claims := token.Claims.(jwt.MapClaims)
		uid := claims["sub"].(string)
		issuer := claims["issuer"].(string)
		role := claims["role"].(string)
		w.Header().Set("x-auth-uid", uid)
		w.Header().Set("x-auth-issuer", issuer)
		w.Header().Set("x-auth-role", role)
		return
	})
```

ここからは、`http://auth/validate` へのリクエストに対するレスポンスが 2xx で終了するには、`auth_token` なる Cookie にセットされた JWT がいくつかの validation を通過する必要があることが分かる。また JWT の `role` クレームの値が `x-auth-role` ヘッダに設定されていることがわかる。

以上を整理すると、この問題でフラグに至るまでの経路は、およそ以下のような形になることがわかる。

1. `role` クレームに値 `admin` を持ち、かつ `auth/main.go` 内の validation をなんとか通過するような JWT を生成する
2. その JWT を `auth_token` Cookie に乗せて nginx に向けて送る

## `auth/main.go` 内の validation のバイパス

`auth/main.go` 内の validation とは、以下のようなものであった。

```go
		token, err := jwt.Parse(authToken, generateKeySelector(publicKey))
		if err != nil {
			// auth token is weird.
			w.WriteHeader(http.StatusUnauthorized)
			return
		}

		if ok := validateTokenHeader(token, rootPool); !ok {
			// the header seems to be broken.
			w.WriteHeader(http.StatusForbidden)
			return
		}

		if !token.Valid {
			// the signature is broken.
			w.WriteHeader(http.StatusForbidden)
			return
		}
```		

ここで、これらを大まかに読むと、以下のようなことがわかる。

- `generateKeySelector(defaultKey)` は、「`extractCertificateChainFromHeader()` により JWT のヘッダ部分に証明書情報が見つかれば、そこから JWT の署名に使われている鍵を抽出して返す。さもなくば `defaultKey` を返す」という関数を返す。
- `validateTokenHeader()` は、些末な検証の後、`extractCertificateChainFromHeader()` により JWT のヘッダ部分に証明書情報が見つかれば、その証明書が root CA (`/cert/root.crt`) から（直接的に、あるいは間接的に）信頼されているかを検証する。すべての検証をクリアした場合に真を返す。
- `token.Valid` は、先ほどの `generateKeySelector()` により生成された関数に `token` を渡した際に得られた鍵が、正しく `token` の署名を検証した場合に真になる。

つまり、サービス `auth` は、自分自身（`auth`）が発行した JWT か、自分自身が持つ Root CA により信頼されている証明書に紐づいた秘密鍵により生成された JWT の二種のみを受理しようとしている。しかし、これが本当に成り立っているとしたら、JWT のクレームの改ざんはかなり難しい。例えば以下のようなことが言えてしまう。

1. `x5u` / `x5c` のようなパラメータが JWT のヘッダ中にない場合は、`auth` が管理している公開鍵で JWT を検証するので、改ざんにはその公開鍵に対応する秘密鍵のリークが必要になる。
2. `x5u` / `x5c` のようなパラメータが JWT のヘッダ中にある場合には、そこに指定されたパラメータが Root CA により信頼されている必要があるので、Root CA の持つ秘密鍵のリークが必要になる。

これは pwn ではないので、これらの方針は、たぶんない。

## 天下りで頑張る

理詰めで説明を書こうと思ったが、もう飽きたので、天下りで説明することにする。

`generateKeySelector(defaultKey)` と `validateTokenHeader()` はともに `extractCertificateChainFromHeader()` を呼ぶ。なんかこの辺を睨むと回答に到達する

```sh
openssl genrsa -out solver.key 4096
openssl req -x509 -new -nodes -key solver.key -sha256 -days 1024 -out solver.crt 
```