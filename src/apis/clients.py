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

import os
import httpx
from typing import Generator


def __get_client(env_api_prefix: str) -> Generator[httpx.Client, None, None]:
    base_url = os.getenv(env_api_prefix + "_API_BASE_URL")
    client = httpx.Client(base_url=base_url)
    try:
        yield client
    finally:
        client.close()


def pet_store_api() -> Generator[httpx.Client, None, None]:
    yield from __get_client("PET_STORE")


def pets_api() -> Generator[httpx.Client, None, None]:
    yield from __get_client("PETS")


def customers_api() -> Generator[httpx.Client, None, None]:
    yield from __get_client("CUSTOMERS")


def orders_api() -> Generator[httpx.Client, None, None]:
    yield from __get_client("ORDERS")
