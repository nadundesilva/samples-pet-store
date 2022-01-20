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

from typing import List, Union
from fastapi import Depends, FastAPI, status
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK
from data.database import db_session
from data import schemas
from . import crud
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

app = FastAPI(root_path="/orders")


@app.get("/health", response_model=schemas.Health, status_code=status.HTTP_200_OK)
def check_health():
    return schemas.Health(status=schemas.HealthStatus.ready)


@app.get("/", response_model=List[schemas.Order], status_code=HTTP_200_OK)
def get_orders(
    customer_id: int, db: Session = Depends(db_session)
) -> List[schemas.Order]:
    return crud.get_orders(db, customer_id)


@app.post(
    "/",
    response_model=Union[schemas.Order, schemas.Error],
    status_code=status.HTTP_200_OK,
)
def add_order(order: schemas.Order, db: Session = Depends(db_session)) -> schemas.Order:
    if order.id is not None:
        return schemas.Error(message="ID for new orders should not be specified")
    if order.creation_timestamp is not None:
        return schemas.Error(
            message="Creation timestamp for new orders should not be specified"
        )
    if order.payment_timestamp is not None:
        return schemas.Error(
            message="Payment timestamp for new orders should not be specified"
        )

    return crud.create_order(db, order=order)


@app.post(
    "/{order_id}/items",
    response_model=Union[schemas.OrderItem, schemas.Error],
    status_code=status.HTTP_200_OK,
)
def add_order_item(
    order_id: int, order_item: schemas.OrderItem, db: Session = Depends(db_session)
):
    if order_item.id is not None:
        return schemas.Error(message="ID for new order items should not be specified")

    overriden_order_item = order_item.dict()
    overriden_order_item["order_id"] = order_id
    order_item = schemas.OrderItem(**overriden_order_item)
    return crud.create_order_item(db, order_item)


FastAPIInstrumentor.instrument_app(app)
