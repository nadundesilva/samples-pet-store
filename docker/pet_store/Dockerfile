FROM nadunrds/samples-pet-store-builder-base:latest as builder

WORKDIR /app

COPY . /app

RUN python3 -m build

FROM nadunrds/samples-pet-store-runtime-base:latest

WORKDIR /app
EXPOSE 8080

COPY --from=builder /app/dist/pet_store_sample-*.whl /app
COPY ./docker/pet_store/entrypoint.sh /app/entrypoint.sh

RUN pip install /app/pet_store_sample-*.whl \
    && rm /app/pet_store_sample-*.whl

ENTRYPOINT [ "bash", "entrypoint.sh" ]
