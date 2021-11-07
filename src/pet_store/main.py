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
from typing import Dict, List, Union
from fastapi import FastAPI
from data import schemas
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


@app.get("/health", response_model=schemas.Health, status_code=status.HTTP_200_OK)
def check_health(
    response: Response,
    pets_api_connection: HTTPConnection = Depends(connections.pets_api),
    customers_api_connection: HTTPConnection = Depends(connections.customers_api),
    orders_api_connection: HTTPConnection = Depends(connections.orders_api),
) -> schemas.Health:
    dependency_connections = {
        "pets-api": pets_api_connection,
        "customers-api": customers_api_connection,
        "orders-api": orders_api_connection,
    }

    api_status = schemas.HealthStatus.ready
    dependencies: Dict[str, schemas.Health] = {}
    for api_name, connection in dependency_connections.items():
        dependency_status, status_code = api_client.call(
            connection, "GET", "/health", schemas.Health
        )
        if api_status == schemas.HealthStatus.ready and (
            status_code != 200 or dependency_status.status != schemas.HealthStatus.ready
        ):
            api_status = schemas.HealthStatus.unavailable
            response.status_code = 503

        if status_code == 200:
            dependencies[api_name] = dependency_status
        else:
            dependencies[api_name] = schemas.Health(
                status=schemas.HealthStatus.unavailable
            )

    return schemas.Health(status=api_status, dependencies=dependencies)


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
        schemas.Pet,
    )
    logger.debug("Found " + str(len(pets)) + " available pets")
    return pets


@app.post("/catalog", response_model=schemas.Pet, status_code=status.HTTP_200_OK)
def add_pet(
    response: Response,
    pet: schemas.Pet,
    pets_api_connection: HTTPConnection = Depends(connections.pets_api),
) -> schemas.Pet:
    created_pet, status_code = api_client.call(
        pets_api_connection, "POST", "/", schemas.Pet, pet
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
        return schemas.Error(message="Failed to create catalog item")
    return created_pet


@app.post("/customers", response_model=schemas.Customer, status_code=status.HTTP_200_OK)
def add_customer(
    response: Response,
    customer: schemas.Customer,
    customers_api_connection: HTTPConnection = Depends(connections.customers_api),
) -> schemas.Customer:
    created_customer, status_code = api_client.call(
        customers_api_connection, "POST", "/", schemas.Customer, customer
    )
    response.status_code = status_code
    if status_code == 200:
        logger.debug("Created a new customer with ID " + str(created_customer.id))
    else:
        logger.error(
            "Failed to create a new customer with status code " + str(status_code)
        )
        return schemas.Error(message="Failed to create customer")

    return created_customer


@app.post("/orders", response_model=schemas.Order, status_code=status.HTTP_200_OK)
def add_order(
    response: Response,
    order: schemas.Order,
    orders_api_connection: HTTPConnection = Depends(connections.orders_api),
) -> schemas.Order:
    created_order, status_code = api_client.call(
        orders_api_connection,
        "POST",
        "/",
        schemas.Order,
        order,
    )
    response.status_code = status_code
    if status_code == 200:
        logger.debug("Created a new order with ID " + str(created_order.id))
    else:
        logger.error(
            "Failed to create a new order with status code " + str(status_code)
        )
        return schemas.Error(message="Failed to create order")

    return created_order


@app.post(
    "/orders/{order_id}/items",
    response_model=Union[schemas.OrderItem, schemas.Error],
    status_code=status.HTTP_200_OK,
)
def add_order_item(
    response: Response,
    order_id: int,
    pet_id: int,
    amount: int = Query(default=1, gt=0),
    pets_api_connection: HTTPConnection = Depends(connections.pets_api),
    orders_api_connection: HTTPConnection = Depends(connections.orders_api),
) -> schemas.Order:
    reservation, status_code = api_client.call(
        pets_api_connection,
        "PATCH",
        "/"
        + parse.quote(str(pet_id))
        + "/reservation?amount="
        + parse.quote(str(amount)),
        schemas.Reservation,
    )
    response.status_code = status_code
    if status_code != 200:
        logger.debug(
            "Creation of order item with ID "
            + str(order_id)
            + " failed due to pet with ID "
            + str(pet_id)
            + " not found"
        )
        return schemas.Error(message="Pet with ID " + str(pet_id) + " not found")
    elif reservation.status == schemas.HealthStatus.unavailable:
        logger.debug(
            "Creation of order item with ID "
            + str(order_id)
            + " failed due to pet with ID "
            + str(pet_id)
            + " being out of stock"
        )
        return schemas.Error(message="Pet with ID " + str(pet_id) + " out of stock")

    order_item = schemas.OrderItem(
        pet_id=pet_id,
        order_id=order_id,
        amount=amount,
        unit_price=reservation.pet.current_price,
    )
    created_order, status_code = api_client.call(
        orders_api_connection,
        "POST",
        "/" + parse.quote(str(order_id)) + "/items",
        schemas.OrderItem,
        order_item,
    )
    response.status_code = status_code
    if status_code == 200:
        logger.debug("Created a new order with ID " + str(created_order.id))
    else:
        logger.error(
            "Failed to create a new order with status code " + str(status_code)
        )
        return schemas.Error(message="Failed to create order item")

    return created_order
