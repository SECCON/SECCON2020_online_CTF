FROM python:3.8-alpine as dep
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

FROM python:3.8-alpine as prod
COPY --from=dep /usr/local/lib/python3.8/ /usr/local/lib/python3.8/
COPY exploit.py exploit.py
CMD [ "python", "exploit.py" ]
