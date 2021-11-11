FROM python:3.10.0

WORKDIR /app

COPY . /app

RUN pip install --upgrade build \
    && pip install -e . \
    && rm -rf /app
