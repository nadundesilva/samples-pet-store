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
from http.client import HTTPConnection
from typing import Generator


def __get_connection(env_api_prefix: str) -> Generator[HTTPConnection, None, None]:
    connection = HTTPConnection(
        os.getenv(env_api_prefix + "_API_HOST"),
        int(os.getenv(env_api_prefix + "_API_PORT")),
        timeout=10,
    )
    try:
        yield connection
    finally:
        connection.close()


def pet_store_api() -> Generator[HTTPConnection, None, None]:
    yield from __get_connection("PET_STORE")


def pets_api() -> Generator[HTTPConnection, None, None]:
    yield from __get_connection("PETS")


def customers_api() -> Generator[HTTPConnection, None, None]:
    yield from __get_connection("CUSTOMERS")
