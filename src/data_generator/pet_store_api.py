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

from typing import Any, Type
from data import convert
from apis import connections, client as api_client


def call(method: str, url: str, object_type: Type[Any], body: Any = None) -> Any:
    connection = next(connections.pet_store_api())
    body_bytes = bytes(convert.to_json(body), "utf-8") if body is not None else None
    response_body, status_code = api_client.call(
        connection, method, url, body=body_bytes, object_type=object_type
    )
    if status_code != 200:
        raise Exception(
            "Failed to call Pet Store API with status code " + str(status_code)
        )
    return response_body
