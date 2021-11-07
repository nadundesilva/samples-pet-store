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

from sqlalchemy.orm import Session
from . import db_models as models
from data import schemas


def create_order(db: Session, order: schemas.Order) -> schemas.Order:
    db_order = models.Order(customer_id=order.customer_id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return schemas.Order.from_orm(db_order)


def create_order_item(db: Session, order_item: schemas.OrderItem):
    db_order_item = models.OrderItem(
        pet_id=order_item.pet_id,
        order_id=order_item.order_id,
        amount=order_item.amount,
        unit_price=order_item.unit_price,
    )
    db.add(db_order_item)
    db.commit()
    db.refresh(db_order_item)
    return schemas.OrderItem.from_orm(db_order_item)
