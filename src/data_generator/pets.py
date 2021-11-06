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
from .pet_store_api import call_api
from data import schemas


logger = logging.getLogger(__name__)


def __get_all_pets() -> bool:
    return call_api("GET", "/catalog", schemas.Pet)


def __create_pet(pet: schemas.Pet) -> schemas.Pet:
    return call_api("POST", "/", schemas.Pet, pet)


def generate() -> List[schemas.Pet]:
    db_pets = __get_all_pets()
    if len(db_pets) > 0:
        logger.warning(
            "Pet data not genreated as "
            + str(len(db_pets))
            + " pet(s) is already present in DB"
        )
        return db_pets

    pets = []
    pets.append(
        __create_pet(
            schemas.Pet(
                display_name="Labrador Retriever",
                kind="Dog",
                current_price=1000,
                available_amount=3,
            )
        )
    )
    pets.append(
        __create_pet(
            schemas.Pet(
                display_name="Golden Retriever",
                kind="Dog",
                current_price=1500,
                available_amount=7,
            )
        )
    )
    pets.append(
        __create_pet(
            schemas.Pet(
                display_name="German Shepherd",
                kind="Dog",
                current_price=1400,
                available_amount=5,
            )
        )
    )
    pets.append(
        __create_pet(
            schemas.Pet(
                display_name="Pembroke Welsh Corgi",
                kind="Dog",
                current_price=1600,
                available_amount=3,
            )
        )
    )
    pets.append(
        __create_pet(
            schemas.Pet(
                display_name="Savannah",
                kind="Cat",
                current_price=15000,
                available_amount=2,
            )
        )
    )
    pets.append(
        __create_pet(
            schemas.Pet(
                display_name="Bengal",
                kind="Cat",
                current_price=1300,
                available_amount=4,
            )
        )
    )
    pets.append(
        __create_pet(
            schemas.Pet(
                display_name="Common Goldfish",
                kind="Fish",
                current_price=30,
                available_amount=50,
            )
        )
    )
    pets.append(
        __create_pet(
            schemas.Pet(
                display_name="Corydoras Catfish",
                kind="Fish",
                current_price=25,
                available_amount=20,
            )
        )
    )
    pets.append(
        __create_pet(
            schemas.Pet(
                display_name="Syrian Hamster",
                kind="Hamster",
                current_price=13,
                available_amount=10,
            )
        )
    )

    db_pets = __get_all_pets()
    if len(db_pets) != len(pets):
        raise Exception("Data inconsistency in generated pets")
    logger.info("Generated pets sample data completed")
    return pets
