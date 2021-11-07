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
from typing import List
from .pet_store_api import call as call_api
from data import schemas

logger = logging.getLogger(__name__)


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


def __generate_orders_items(orders: List[schemas.Order], pets: List[schemas.Pet]):
    order_items = []
    return order_items


def generate(
    customers: List[schemas.Customer], pets: List[schemas.Pet]
) -> List[schemas.Order]:
    orders = __generate_orders(customers)
    orders_items = __generate_orders_items(orders, pets)
    return orders, orders_items
