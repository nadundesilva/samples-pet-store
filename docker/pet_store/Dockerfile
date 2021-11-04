FROM python:3.9.7 as builder

WORKDIR /app

COPY . /app

RUN pip install --upgrade build
RUN python3 -m build

FROM python:3.9.7

WORKDIR /app
EXPOSE 8080

COPY --from=builder /app/dist/pet_store_sample-*.whl /app

RUN pip install /app/pet_store_sample-*.whl && \
    rm /app/pet_store_sample-*.whl && \
    pip install --upgrade uvicorn==0.15.0

ENTRYPOINT [ "uvicorn", "pet_store.main:app", "--host", "0.0.0.0", "--port", "8080" ]
