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
import telemetry
import httpx
from typing import Tuple, Type
from pydantic import BaseModel

logger = telemetry.get_logger(__name__)


def call(
    client: httpx.Client,
    method: str,
    url: str,
    model_type: Type[BaseModel],
    body: BaseModel = None,
) -> Tuple[BaseModel, int]:
    headers = {"Accept": "application/json"}
    if body is not None:
        headers["Content-Type"] = "application/json"

    response = client.request(
        method,
        url,
        content=(None if body is None else bytes(body.json(), "utf-8")),
        headers=headers,
    )
    if response.status_code == 200:
        logger.debug(
            "Received response for API call "
            + method
            + " "
            + url
            + " with status code "
            + str(response.status_code)
        )

        response_body = response.read()
        parsed_body = json.loads(response_body)
        if isinstance(parsed_body, list):
            return [
                model_type(**parsed_body_item) for parsed_body_item in parsed_body
            ], response.status_code
        else:
            return model_type(**parsed_body), response.status_code
    else:
        logger.error(
            "API call "
            + method
            + " "
            + url
            + " failed with status code "
            + str(response.status_code)
            + " and response body "
            + str(response.read())
        )
        return None, response.status_code
