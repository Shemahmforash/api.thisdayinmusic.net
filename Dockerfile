FROM python:3.11.0b5

ENV PYTHONUNBUFFERED 1

COPY . /code/
COPY ./.env.example /.env

WORKDIR /code/

RUN pip install pipenv
RUN pipenv install --system --dev

EXPOSE 5000
