FROM python:3.10

RUN mkdir /app

WORKDIR /app

COPY requirements .

RUN pip install -r prod.txt

COPY . .

