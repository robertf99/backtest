FROM python:3.8-slim-buster

RUN apt-get update
RUN apt-get install -y curl

RUN pip install pipenv
WORKDIR /backtest
COPY ./api/Pipfile* ./api/
WORKDIR /backtest/api

RUN pipenv install --system --skip-lock

COPY ./api .

CMD python -m uvicorn app.main:app --host=0.0.0.0 --port=5000 --log-level=debug