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

import telemetry
from urllib import parse
import httpx
from fastapi import Depends, FastAPI, Query, Response, status
from fastapi.openapi.utils import get_openapi
from typing import Dict, List, Union
from fastapi import FastAPI
from data import schemas
from apis import clients, call as call_api
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry import trace

logger = telemetry.get_logger(__name__)

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
    pets_api_client: httpx.Client = Depends(clients.pets_api),
    customers_api_client: httpx.Client = Depends(clients.customers_api),
    orders_api_client: httpx.Client = Depends(clients.orders_api),
) -> schemas.Health:
    dependency_clients = {
        "pets-api": pets_api_client,
        "customers-api": customers_api_client,
        "orders-api": orders_api_client,
    }

    api_status = schemas.HealthStatus.ready
    dependencies: Dict[str, schemas.Health] = {}
    for api_name, client in dependency_clients.items():
        dependency_status, status_code = call_api(
            client, "GET", "/health", schemas.Health
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
    pets_api_client: httpx.Client = Depends(clients.pets_api),
) -> List[schemas.Pet]:
    pets, response.status_code = call_api(
        pets_api_client,
        "GET",
        "/?limit=" + parse.quote(str(limit)) + "&offset=" + parse.quote(str(offset)),
        schemas.Pet,
    )
    logger.debug("Found " + str(len(pets)) + " available pets")
    return pets


@app.get("/orders", response_model=List[schemas.Order], status_code=status.HTTP_200_OK)
def get_all_orders(
    response: Response,
    customer_id: int,
    orders_api_client: httpx.Client = Depends(clients.orders_api),
) -> List[schemas.Order]:
    trace.get_current_span().set_attribute("pet_store.customer_id", customer_id)
    orders, response.status_code = call_api(
        orders_api_client,
        "GET",
        "/?customer_id=" + parse.quote(str(customer_id)),
        schemas.Order,
    )
    logger.debug(
        "Found " + str(len(orders)) + " orders of customer " + str(customer_id)
    )
    return orders


@app.post("/catalog", response_model=schemas.Pet, status_code=status.HTTP_200_OK)
def add_pet(
    response: Response,
    pet: schemas.Pet,
    pets_api_client: httpx.Client = Depends(clients.pets_api),
) -> schemas.Pet:
    created_pet, status_code = call_api(pets_api_client, "POST", "/", schemas.Pet, pet)
    response.status_code = status_code
    if status_code == 200:
        trace.get_current_span().set_attribute("pet_store.pet_id", created_pet.id)
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
    customers_api_client: httpx.Client = Depends(clients.customers_api),
) -> schemas.Customer:
    created_customer, status_code = call_api(
        customers_api_client, "POST", "/", schemas.Customer, customer
    )
    response.status_code = status_code
    if status_code == 200:
        trace.get_current_span().set_attribute(
            "pet_store.customer_id", created_customer.id
        )
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
    orders_api_client: httpx.Client = Depends(clients.orders_api),
) -> schemas.Order:
    created_order, status_code = call_api(
        orders_api_client,
        "POST",
        "/",
        schemas.Order,
        order,
    )
    response.status_code = status_code
    if status_code == 200:
        trace.get_current_span().set_attribute("pet_store.order_id", created_order.id)
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
    pets_api_client: httpx.Client = Depends(clients.pets_api),
    orders_api_client: httpx.Client = Depends(clients.orders_api),
) -> schemas.Order:
    trace.get_current_span().set_attribute("pet_store.order_id", order_id)
    reservation, status_code = call_api(
        pets_api_client,
        "PATCH",
        "/"
        + parse.quote(str(pet_id))
        + "/reservation?amount="
        + parse.quote(str(amount)),
        schemas.Reservation,
    )
    response.status_code = status_code
    if status_code != 200:
        trace.get_current_span().set_attribute(
            "pet_store.reservation_status", reservation.status
        )
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
    created_order_item, status_code = call_api(
        orders_api_client,
        "POST",
        "/" + parse.quote(str(order_id)) + "/items",
        schemas.OrderItem,
        order_item,
    )
    response.status_code = status_code
    if status_code == 200:
        trace.get_current_span().set_attribute(
            "pet_store.order_item_id", created_order_item.id
        )
        logger.debug("Created a new order with ID " + str(created_order_item.id))
    else:
        logger.error(
            "Failed to create a new order with status code " + str(status_code)
        )
        return schemas.Error(message="Failed to create order item")

    return created_order_item


FastAPIInstrumentor.instrument_app(app)
