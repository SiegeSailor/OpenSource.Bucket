FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /source/

COPY ./requirements.txt /source/

RUN pip install --no-cache-dir --requirements requirements.txt

COPY . /source/