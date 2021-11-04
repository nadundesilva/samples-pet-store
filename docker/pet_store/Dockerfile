FROM python:3.9.7 as builder

WORKDIR /app

COPY . /app

RUN pip install --upgrade build
RUN python3 -m build

FROM python:3.9.7

WORKDIR /app
EXPOSE 8080
ENV DOCKERIZE_VERSION v0.6.1

COPY --from=builder /app/dist/pet_store_sample-*.whl /app
COPY ./docker/pet_store/entrypoint.sh /app/entrypoint.sh

RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && pip install /app/pet_store_sample-*.whl \
    && rm /app/pet_store_sample-*.whl \
    && pip install --upgrade uvicorn==0.15.0

ENTRYPOINT [ "bash", "entrypoint.sh" ]
