"""Copyright (c) 2021, Deep Net. All Rights Reserved.

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

import json
import os
from urllib import parse
from http.client import HTTPConnection
from fastapi import Depends, FastAPI, Query, Response, status
from fastapi.openapi.utils import get_openapi
from typing import Any, List, Type
from fastapi import FastAPI
from database import schemas

app = FastAPI()


def get_open_api_schema():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Pet Store API",
        version="1.0.0",
        description="Pet Store Sample API",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = get_open_api_schema


def get_pets_api_connection():
    connection = HTTPConnection(
        os.getenv("PETS_API_HOST"), int(os.getenv("PETS_API_PORT")), timeout=10
    )
    try:
        yield connection
    finally:
        connection.close()


def parse_client_response(
    connection: HTTPConnection, incoming_req_response: Response, type: Type[Any]
):
    client_response = connection.getresponse()
    incoming_req_response.status_code = client_response.status
    if client_response.status == status.HTTP_200_OK:
        return json.loads(client_response.read(), object_hook=lambda d: type(**d))
    return None


@app.get("/health")
def check_health():
    return {"status": "Ready"}


@app.get("/catalog", response_model=List[schemas.Pet], status_code=status.HTTP_200_OK)
def get_pets_catalog(
    response: Response,
    limit: int = Query(default=100, lte=100),
    offset: int = 0,
    pets_api_connection: HTTPConnection = Depends(get_pets_api_connection),
) -> List[schemas.Pet]:
    pets_api_connection.request(
        "GET",
        "/catalog?limit="
        + parse.quote(str(limit))
        + "&offset="
        + parse.quote(str(offset)),
    )
    return parse_client_response(pets_api_connection, response, List[schemas.Pet])


@app.post("/", response_model=schemas.Pet, status_code=status.HTTP_200_OK)
def add_pet(
    response: Response,
    pet: schemas.Pet,
    pets_api_connection: HTTPConnection = Depends(get_pets_api_connection),
) -> schemas.Pet:
    pets_api_connection.request("POST", "/", body=pet)
    return parse_client_response(pets_api_connection, response, schemas.Pet)
