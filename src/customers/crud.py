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

from sqlalchemy.orm import Session
from . import db_models as models
from data import schemas


def create_customer(db: Session, customer: schemas.Customer) -> schemas.Customer:
    db_customer = models.Customer(
        first_name=customer.first_name,
        last_name=customer.last_name,
        delivery_address=customer.delivery_address,
        contact_number=customer.contact_number,
    )
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return schemas.Customer.from_orm(db_customer)
