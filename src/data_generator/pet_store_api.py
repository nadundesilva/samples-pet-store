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
import json
import os
from http.client import HTTPConnection
from typing import Any, Type


def call_api(method: str, url: str, type: Type[Any], body: Any = None):
    connection = HTTPConnection(
        os.getenv("PET_STORE_API_HOST"),
        int(os.getenv("PET_STORE_API_PORT")),
        timeout=10,
    )
    try:
        body_bytes = bytes(json.dumps(dict(body)), "utf-8") if body is not None else None
        connection.request(method, url, body=body_bytes)
        response = connection.getresponse()
        if response.status != 200:
            raise Exception("Failed to call Pet Store API with status code " + str(response.status))

        return json.loads(response.read(), object_hook=lambda d: type(**d))
    finally:
        connection.close()
