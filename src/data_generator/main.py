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

from apis import clients
import telemetry
from . import pets, customers, orders

logger = telemetry.get_logger(__name__)


def generate_data() -> None:
    with clients.pet_store_api_client_context() as client:
        logger.info("Generating sample data started")
        created_pets = pets.generate(client)
        created_customers = customers.generate(client)
        orders.generate(client, created_customers, created_pets)
        logger.info("Generating sample data completed")
