FROM python:3.9.7

WORKDIR /app
ENV DOCKERIZE_VERSION v0.6.1

COPY . /app

RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && pip install --upgrade uvicorn==0.15.0 \
    && pip install -e . \
    && rm -rf /app
