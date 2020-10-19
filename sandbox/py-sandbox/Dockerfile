FROM python:2.7.16

RUN apt-get update && \
        apt-get -y upgrade && \
        apt-get install -y \
            xinetd \
            iproute2

RUN groupadd -r user && useradd -r -g user user

COPY --chown=root:user ./build/start.sh /home/user/start.sh
COPY --chown=root:root ./build/ctf.conf /etc/xinetd.d/ctf
COPY --chown=root:user ./build/flag /home/user/flag
COPY --chown=root:user ./dist/run.py /home/user/run.py

WORKDIR /home/user

RUN chmod 444 ./flag && \
    chmod 555 ./run.py && \
    chmod 555 ./start.sh && \
    chmod 444 /etc/xinetd.d/ctf

RUN mv ./flag flag-$(md5sum ./flag | awk '{print $1}')

USER user
EXPOSE 30002

ENV  PYTHONUNBUFFERED=x

CMD ["xinetd","-dontfork","-f","/etc/xinetd.d/ctf"]

