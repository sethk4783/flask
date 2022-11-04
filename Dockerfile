# FROM python:3.10

# RUN pip install --upgrade pip
# RUN pip install --no-cache-dir -r requirements.txt

# ENV PYTHONUNBUFFERED=1

# ENV FLASK_APP=server.py
# ENV FLASK_ENV=development
# ENV FLASK_DEBUG=1

# CMD ["flask", "run"]

# # EXPOSE 5000

# FROM python:3

FROM python:3.10.6-slim-buster

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update  && \
    apt-get install -yq libmariadb3 libmariadb-dev

RUN rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=server.py
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1

WORKDIR /code

COPY requirements.txt /code

RUN pip install -r requirements.txt

COPY . /code/
