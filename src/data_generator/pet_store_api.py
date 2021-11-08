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
from typing import Type
from apis import call as call_api
from pydantic import BaseModel


def call(
    method: str, url: str, model_type: Type[BaseModel], body: BaseModel = None
) -> BaseModel:
    with httpx.Client(base_url=os.getenv("PET_STORE_API_BASE_URL")) as client:
        response_body, status_code = call_api(client, method, url, model_type, body)
        if status_code != 200:
            raise Exception(
                "Failed to call Pet Store API with status code "
                + str(status_code)
                + " for "
                + method
                + " "
                + url
            )
        return response_body
