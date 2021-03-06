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

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

OTEL_VERSION = "1.11.0"
OTEL_AUTO_INST_VERSION = "0.30b1"

setuptools.setup(
    name="pet-store-sample",
    version="0.1.0",
    author="Nadun De Silva",
    author_email="nadunrds@gmail.com",
    description="A sample Pet Store application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nadundesilva/samples-pet-store",
    project_urls={
        "Bug Tracker": "https://github.com/nadundesilva/samples-pet-store/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    setup_requires=["pytest-runner"],
    install_requires=[
        "fastapi ~= 0.78.0",
        "SQLAlchemy ~= 1.4.37",
        "PyMySQL ~= 1.0.2",
        "cryptography ~= 37.0.2",
        "httpx ~= 0.23.0",
        "python-json-logger ~= 2.0.2",
        "opentelemetry-api ~= " + OTEL_VERSION,
        "opentelemetry-sdk ~= " + OTEL_VERSION,
        "opentelemetry-instrumentation-fastapi ~= " + OTEL_AUTO_INST_VERSION,
        "opentelemetry-instrumentation-sqlalchemy ~= " + OTEL_AUTO_INST_VERSION,
        "opentelemetry-instrumentation-logging ~= " + OTEL_AUTO_INST_VERSION,
        "opentelemetry-instrumentation-httpx ~= " + OTEL_AUTO_INST_VERSION,
        "opentelemetry-propagator-b3 ~= " + OTEL_VERSION,
        "opentelemetry-exporter-otlp-proto-grpc ~= " + OTEL_VERSION,
    ],
    tests_require=["pytest ~= 7.1.2", "coverage ~= 6.4.1"],
    extras_require={
        "dev": ["black ~= 22.3.0"],
        "prod": ["uvicorn==0.17.6", "gunicorn ~= 20.1.0"],
    },
)
