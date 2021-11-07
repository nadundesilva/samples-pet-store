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

import datetime
from typing import Optional
from pydantic import BaseModel


class Pet(BaseModel):
    id: Optional[int]
    display_name: str
    kind: str
    current_price: int
    available_amount: Optional[int]


class Customer(BaseModel):
    id: Optional[int]
    first_name: str
    last_name: str
    delivery_address: str
    contact_number: str


class Order(BaseModel):
    id: Optional[int]
    customer_id: int
    creation_timestamp: Optional[datetime.datetime]
    payment_timestamp: Optional[datetime.datetime]


class OrderItem(BaseModel):
    id: Optional[int]
    pet_id: int
    order_id: int
    amount: int
    unit_price: int
