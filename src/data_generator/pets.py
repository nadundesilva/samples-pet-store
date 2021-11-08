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

import httpx
import telemetry
from typing import List
from .pet_store_api import call as call_api
from data import schemas

logger = telemetry.get_logger(__name__)


def __create_pet(client: httpx.Client, pet: schemas.Pet) -> schemas.Pet:
    return call_api(client, "POST", "/catalog", schemas.Pet, pet)


def generate(client: httpx.Client) -> List[schemas.Pet]:
    pets = [
        __create_pet(
            client,
            schemas.Pet(
                display_name="Labrador Retriever",
                kind="Dog",
                current_price=1000.00,
                available_amount=3,
            ),
        ),
        __create_pet(
            client,
            schemas.Pet(
                display_name="Golden Retriever",
                kind="Dog",
                current_price=1500.00,
                available_amount=7,
            ),
        ),
        __create_pet(
            client,
            schemas.Pet(
                display_name="German Shepherd",
                kind="Dog",
                current_price=1400.00,
                available_amount=5,
            ),
        ),
        __create_pet(
            client,
            schemas.Pet(
                display_name="Pembroke Welsh Corgi",
                kind="Dog",
                current_price=1600.00,
                available_amount=3,
            ),
        ),
        __create_pet(
            client,
            schemas.Pet(
                display_name="Savannah",
                kind="Cat",
                current_price=15000.00,
                available_amount=2,
            ),
        ),
        __create_pet(
            client,
            schemas.Pet(
                display_name="Bengal",
                kind="Cat",
                current_price=1300.00,
                available_amount=4,
            ),
        ),
        __create_pet(
            client,
            schemas.Pet(
                display_name="Common Goldfish",
                kind="Fish",
                current_price=30.00,
                available_amount=50,
            ),
        ),
        __create_pet(
            client,
            schemas.Pet(
                display_name="Corydoras Catfish",
                kind="Fish",
                current_price=25.00,
                available_amount=20,
            ),
        ),
        __create_pet(
            client,
            schemas.Pet(
                display_name="Syrian Hamster",
                kind="Hamster",
                current_price=13.00,
                available_amount=10,
            ),
        ),
    ]
    logger.info("Generating " + str(len(pets)) + " sample pet(s) completed")
    return pets
