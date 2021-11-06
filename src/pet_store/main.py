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

import logging
from urllib import parse
from http.client import HTTPConnection
from fastapi import Depends, FastAPI, Query, Response, status
from fastapi.openapi.utils import get_openapi
from typing import Dict, List, Literal, TypedDict, Union
from fastapi import FastAPI
from data import schemas
from data import convert
from apis import connections, client as api_client

logger = logging.getLogger(__name__)

app = FastAPI()


def __get_open_api_schema():
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


app.openapi = __get_open_api_schema


class HealthStatus(TypedDict):
    status: Union[Literal["Ready"], Literal["Unavailable"]]
    dependencies: Dict[str, "HealthStatus"]


@app.get("/health")
def check_health(
    response: Response,
    pets_api_connection: HTTPConnection = Depends(connections.pets_api),
) -> HealthStatus:
    dependency_connections = {"pets-api": pets_api_connection}

    api_status = "Ready"
    dependency_health: Dict[str, HealthStatus] = {}
    for api_name, connection in dependency_connections.items():
        dependency_status, status_code = api_client.call(connection, "GET", "/health")
        if api_status == "Ready":
            api_status = "Unavailable"
            response.status_code = 503

        if status_code == 200:
            dependency_health[api_name] = dependency_status
        else:
            dependency_health[api_name] = {"status": "Ready"}

    return {"status": "Ready", "dependencies": dependency_health}


@app.get("/catalog", response_model=List[schemas.Pet], status_code=status.HTTP_200_OK)
def get_pets_catalog(
    response: Response,
    limit: int = Query(default=100, lte=100),
    offset: int = 0,
    pets_api_connection: HTTPConnection = Depends(connections.pets_api),
) -> List[schemas.Pet]:
    pets, response.status_code = api_client.call(
        pets_api_connection,
        "GET",
        "/?limit=" + parse.quote(str(limit)) + "&offset=" + parse.quote(str(offset)),
        object_type=schemas.Pet,
    )
    logger.debug("Found " + str(len(pets)) + " available pets")
    return pets


@app.post("/catalog", response_model=schemas.Pet, status_code=status.HTTP_200_OK)
def add_pet(
    response: Response,
    pet: schemas.Pet,
    pets_api_connection: HTTPConnection = Depends(connections.pets_api),
) -> schemas.Pet:
    body = bytes(convert.to_json(pet), "utf-8")
    created_pet, status_code = api_client.call(
        pets_api_connection, "POST", "/", body=body, object_type=schemas.Pet
    )
    response.status_code = status_code
    if status_code == 200:
        logger.debug(
            "Created a new pet "
            + created_pet.display_name
            + " of kind "
            + created_pet.kind
            + " with ID "
            + str(created_pet.id)
        )
    else:
        logger.error(
            "Failed to create a new pet "
            + pet.display_name
            + " of kind "
            + pet.kind
            + " with status code "
            + str(status_code)
        )
    return created_pet


@app.post("/customers", response_model=schemas.Customer, status_code=status.HTTP_200_OK)
def add_customer(
    response: Response,
    customer: schemas.Customer,
    customers_api_connection: HTTPConnection = Depends(connections.customers_api),
) -> schemas.Customer:
    body = bytes(convert.to_json(customer), "utf-8")
    created_customer, status_code = api_client.call(
        customers_api_connection,
        "POST",
        "/",
        body=body,
        object_type=schemas.Customer,
    )
    response.status_code = status_code
    if status_code == 200:
        logger.debug("Created a new customer with ID " + str(created_customer.id))
    else:
        logger.error(
            "Failed to create a new customer with status code " + str(status_code)
        )

    return created_customer
