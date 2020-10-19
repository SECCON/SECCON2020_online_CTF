FROM python:3
WORKDIR /usr/src/app
RUN pip install pwntools pytest
COPY test_server.py .
ENTRYPOINT ["pytest"]
