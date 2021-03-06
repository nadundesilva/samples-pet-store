"""Copyright (c) 2021, Nadun De Silva. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
from datetime import datetime
import logging
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.logging import (
    LEVELS,
    LoggingInstrumentor,
    environment_variables,
)
from pythonjsonlogger.jsonlogger import JsonFormatter

LOGGING_FORMAT = (
    "%(timestamp)s %(levelname)s %(name)s %(processName)s %(threadName)s "
    + "%(pathname)s %(lineno)d %(message)s %(otelTraceID)s %(otelSpanID)s "
    + "%(otelServiceName)s"
)


class CustomJsonFormatter(JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get("timestamp"):
            now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            log_record["timestamp"] = now
        if log_record.get("level"):
            record.levelname = log_record["level"]
        else:
            record.levelname = record.levelname.upper()


def init(service_name: str):
    __init_tracing(service_name)
    __init_logging()


def __init_tracing(service_name: str):
    resource = Resource(attributes={"service.name": service_name})
    trace.set_tracer_provider(TracerProvider(resource=resource))

    otlp_exporter = OTLPSpanExporter()
    span_processor = BatchSpanProcessor(otlp_exporter)
    trace.get_tracer_provider().add_span_processor(span_processor)


def __init_logging():
    LoggingInstrumentor().instrument(set_logging_format=False)

    handler = logging.StreamHandler()
    handler.setFormatter(CustomJsonFormatter(LOGGING_FORMAT))

    log_level = LEVELS.get(os.environ.get(environment_variables.OTEL_PYTHON_LOG_LEVEL))
    logging.basicConfig(level=log_level, handlers=[handler], force=True)

    for name in [
        *logging.root.manager.loggerDict.keys(),
        "uvicorn",
        "uvicorn.access",
        "uvicorn.error",
    ]:
        logger = logging.getLogger(name)
        logger.handlers = [handler]
        logger.propagate = False


def get_logger(name):
    return logging.getLogger(name)


def get_tracer(name):
    return trace.get_tracer(name)
