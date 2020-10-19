#!/bin/sh
prompt="Enter baseaddr of libc: Enter base64 payload: "
nc ${SECCON_HOST:-${1:-localhost}} ${SECCON_PORT:-${2:-10000}} < payload | cut -b$((${#prompt}+1))-
