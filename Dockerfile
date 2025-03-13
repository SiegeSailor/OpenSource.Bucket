FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="${PYTHONPATH}:/source/"

WORKDIR /source/

COPY ./requirements.txt /source/requirements.txt

RUN pip install --no-cache-dir --requirement ./requirements.txt

COPY ./source/ /source/