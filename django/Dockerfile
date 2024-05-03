FROM python:3.12.3-slim-bookworm

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Security updates & Update pip and setuptools
RUN apt-get -y update \
    && apt-get -y upgrade \
    && python -m pip install --upgrade pip setuptools \
    && rm -rf /var/lib/apt/lists/*

# Install python requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

# Copy Django files
COPY /django /django
WORKDIR /django

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.11.0/wait /wait
RUN chmod +x /wait
