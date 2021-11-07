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
import logging
from http.client import HTTPConnection
from typing import Tuple, Type
from pydantic import BaseModel

logger = logging.getLogger(__name__)


def call(
    connection: HTTPConnection,
    method: str,
    url: str,
    model_type: Type[BaseModel],
    body: BaseModel = None,
) -> Tuple[BaseModel, int]:
    connection.request(
        method, url, body=(None if body is None else bytes(body.json(), "utf-8"))
    )
    response = connection.getresponse()
    if response.status == 200:
        logger.debug(
            "Received response for API call "
            + method
            + " "
            + url
            + " with status code "
            + str(response.status)
        )

        response_body = response.read()
        parsed_body = json.loads(response_body)
        if isinstance(parsed_body, list):
            return [
                model_type(**parsed_body_item) for parsed_body_item in parsed_body
            ], response.status
        else:
            return model_type(**parsed_body), response.status
    else:
        logger.error(
            "API call "
            + method
            + " "
            + url
            + " failed with status code "
            + str(response.status)
            + " and response body "
            + str(response.read())
        )
        return None, response.status
