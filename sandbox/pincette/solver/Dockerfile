FROM python:3 AS builder
WORKDIR /usr/src/app
COPY test_server.py .
RUN pip install pwntools pytest
RUN TERM=linux ./test_server.py > payload

FROM busybox AS solver
WORKDIR /root
COPY --from=builder /usr/src/app/payload .
COPY send_payload.sh /root
ENTRYPOINT ["/root/send_payload.sh"]
