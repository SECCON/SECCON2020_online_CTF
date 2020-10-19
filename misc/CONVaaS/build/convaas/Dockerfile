FROM python:3.8-alpine as dep
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

FROM python:3.8-alpine as prod
ARG convaas_user=convaas
ARG convaas_uid=1000
ARG convaas_gid=$convaas_uid
ARG convaas_home=/home/$convaas_user
ARG convaas_host="localhost"
ARG convaas_port=53440
ARG convaas_basedir=/tmp/convaas/
COPY --from=dep /usr/local/lib/python3.8/ /usr/local/lib/python3.8/
COPY converter.py $convaas_home/converter.py
COPY server.py $convaas_home/server.py
COPY convaas.yaml $convaas_home/convaas.yaml
COPY flag.txt $convaas_home/flag.txt
RUN adduser -D -h $convaas_home --no-create-home $convaas_user \
    # Deploy the challenge
    && chown root:$convaas_user $convaas_home/converter.py \
    && chown root:$convaas_user $convaas_home/server.py \
    && chown root:$convaas_user $convaas_home/convaas.yaml \
    && chown root:$convaas_user $convaas_home/flag.txt \
    && chmod 0440 $convaas_home/flag.txt

WORKDIR $convaas_home
ENV CONVAAS_USER=$convaas_user
ENV CONVAAS_HOME=$convaas_home
ENV CONVAAS_HOST=$convaas_host
ENV CONVAAS_PORT=$convaas_port
ENV CONVAAS_BASEDIR=$convaas_basedir
EXPOSE ${convaas_port}
CMD [ "python", "server.py" ]
