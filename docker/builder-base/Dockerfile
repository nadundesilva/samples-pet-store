FROM python:3.9.7

WORKDIR /app

COPY . /app

RUN pip install --upgrade build \
    && pip install -e . \
    && rm -rf /app
