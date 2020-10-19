FROM python:3.8

WORKDIR /solver
ADD ./ /solver

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "solver.py"]