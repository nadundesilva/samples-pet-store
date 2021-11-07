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
from typing import Dict, List, Literal, Optional
from pydantic import BaseModel
from enum import Enum
from pydantic.main import Extra
from pydantic.types import conint, constr, condecimal


class BaseSchema(BaseModel):
    class Config:
        validate_all = True
        frozen = True
        use_enum_values = True
        validate_assignment = True
        anystr_strip_whitespace = True
        min_anystr_length = 1


class BaseDataSchema(BaseSchema):
    class Config:
        orm_mode = True


class BaseResponseSchema(BaseSchema):
    class Config:
        extra = Extra.forbid


class Pet(BaseDataSchema):
    id: Optional[conint(strict=True, gt=0)]
    display_name: constr(strict=True, max_length=255)
    kind: constr(strict=True, max_length=255, to_lower=True)
    current_price: condecimal(gt=0, max_digits=13, decimal_places=4)
    available_amount: Optional[conint(strict=True, ge=0)]


class Customer(BaseDataSchema):
    id: Optional[conint(strict=True, gt=0)]
    first_name: constr(strict=True, max_length=255)
    last_name: constr(strict=True, max_length=255)
    delivery_address: constr(strict=True, max_length=255)
    contact_number: constr(
        strict=True, max_length=12, min_length=12, regex="^\+[0-9]{11}$"
    )


class OrderItem(BaseDataSchema):
    id: Optional[conint(strict=True, gt=0)]
    pet_id: conint(strict=True, gt=0)
    order_id: Optional[conint(strict=True, gt=0)]
    amount: conint(strict=True, gt=0)
    unit_price: condecimal(gt=0, max_digits=13, decimal_places=4)


class Order(BaseDataSchema):
    id: Optional[conint(strict=True, gt=0)]
    customer_id: conint(strict=True, gt=0)
    creation_timestamp: Optional[datetime.datetime]
    payment_timestamp: Optional[datetime.datetime]
    items: Optional[List[OrderItem]]


class HealthStatus(str, Enum):
    ready = "READY"
    unavailable = "UNAVAILABLE"


class Health(BaseResponseSchema):
    status: HealthStatus
    dependencies: Dict[str, "Health"] = {}


Health.update_forward_refs()


class ReservationStatus(str, Enum):
    reserved = "RESERVED"
    out_of_stock = "OUT_OF_STOCK"


class Reservation(BaseResponseSchema):
    status: ReservationStatus
    pet: Pet


class Error(BaseResponseSchema):
    status: Literal["ERROR"] = "ERROR"
    message: constr(strict=True, max_length=255)
