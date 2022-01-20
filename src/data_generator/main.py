"""Copyright (c) 2021, Nadun De Silva. All Rights Reserved.

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
tracer = telemetry.get_tracer(__name__)


def generate_data() -> None:
    with tracer.start_as_current_span("generate data") as span:
        with clients.pet_store_api_client_context() as client:
            logger.info("Generating sample data started")

            created_pets = pets.generate(client)
            span.set_attribute("gen.pets_count", len(created_pets))

            created_customers = customers.generate(client)
            span.set_attribute("gen.customers_count", len(created_customers))

            created_orders = orders.generate(client, created_customers, created_pets)
            span.set_attribute("gen.orders_count", len(created_orders))

            logger.info("Generating sample data completed")
