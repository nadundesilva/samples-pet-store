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

import telemetry
from urllib import parse
from typing import List
from .pet_store_api import call as call_api
from data import schemas

logger = telemetry.get_logger(__name__)


def __create_order(order: schemas.Order) -> schemas.Order:
    return call_api("POST", "/orders", schemas.Order, order)


def __generate_orders(customers: List[schemas.Customer]) -> List[schemas.Order]:
    if len(customers) < 4:
        raise Exception(
            "Unexpected number of customers generated for orders; expected 4, but found "
            + str(len(customers))
        )

    orders = [
        __create_order(
            schemas.Order(
                customer_id=customers[0].id,
            )
        ),
        __create_order(
            schemas.Order(
                customer_id=customers[1].id,
            )
        ),
        __create_order(
            schemas.Order(
                customer_id=customers[3].id,
            )
        ),
        __create_order(
            schemas.Order(
                customer_id=customers[0].id,
            )
        ),
    ]
    logger.info("Generating " + str(len(orders)) + " sample order(s) completed")
    return orders


def __create_order_item(order_id: int, pet_id: int, amount: int) -> schemas.Order:
    return call_api(
        "POST",
        "/orders/"
        + parse.quote(str(order_id))
        + "/items?pet_id="
        + parse.quote(str(pet_id))
        + "&amount="
        + parse.quote(str(amount)),
        schemas.OrderItem,
    )


def __generate_orders_items(orders: List[schemas.Order], pets: List[schemas.Pet]):
    if len(orders) < 4:
        raise Exception(
            "Unexpected number of orders generated; expected 4, but found "
            + str(len(orders))
        )
    if len(pets) < 9:
        raise Exception(
            "Unexpected number of orders generated; expected 9, but found "
            + str(len(orders))
        )

    order_items = [
        __create_order_item(orders[0].id, pets[0].id, 1),
        __create_order_item(orders[0].id, pets[6].id, 5),
        __create_order_item(orders[1].id, pets[1].id, 1),
        __create_order_item(orders[1].id, pets[8].id, 1),
        __create_order_item(orders[2].id, pets[1].id, 4),
        __create_order_item(orders[3].id, pets[1].id, 5),
    ]
    logger.info(
        "Generating " + str(len(order_items)) + " sample order item(s) completed"
    )
    return order_items


def generate(
    customers: List[schemas.Customer], pets: List[schemas.Pet]
) -> List[schemas.Order]:
    orders = __generate_orders(customers)
    orders_items = __generate_orders_items(orders, pets)
    return orders, orders_items
