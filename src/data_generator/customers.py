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
from typing import List
from .pet_store_api import call as call_api
from data import schemas

logger = telemetry.get_logger(__name__)


def __create_customer(customer: schemas.Customer) -> schemas.Customer:
    return call_api("POST", "/customers", schemas.Customer, customer)


def generate() -> List[schemas.Customer]:
    customers = [
        __create_customer(
            schemas.Customer(
                first_name="Nadun",
                last_name="De Silva",
                delivery_address="T/12/10, Valor Lane, Star City, USA",
                contact_number="+10019216284",
            )
        ),
        __create_customer(
            schemas.Customer(
                first_name="John",
                last_name="Doe",
                delivery_address="X/34/23, Champion Boulevard, West Kirskey, USA",
                contact_number="+12099216581",
            )
        ),
        __create_customer(
            schemas.Customer(
                first_name="Jane",
                last_name="Foster",
                delivery_address="N/12/41, First Lane, East Kirskey, USA",
                contact_number="+12295236571",
            )
        ),
        __create_customer(
            schemas.Customer(
                first_name="Kyle",
                last_name="Dex",
                delivery_address="T/61/4, Second Lane, Smallville, USA",
                contact_number="+12295236571",
            )
        ),
    ]
    logger.info("Generating " + str(len(customers)) + " sample customer(s) completed")
    return customers
