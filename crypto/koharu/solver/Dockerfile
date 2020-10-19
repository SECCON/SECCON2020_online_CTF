FROM sagemath/sagemath:latest

RUN sage -python -m pip install tqdm

ADD solve.sage solve.sage
ADD output.txt output.txt

ENTRYPOINT sage solve.sage
