FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /source/

COPY ./requirements.txt /source/requirements.txt

RUN pip install --no-cache-dir --requirement ./requirements.txt

COPY ./source/ /source/