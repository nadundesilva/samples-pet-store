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

from typing import Union
from fastapi import Depends, FastAPI, status
from sqlalchemy.orm import Session
from data.database import db_session
from data import schemas
from . import crud
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

app = FastAPI(root_path="/customers")


@app.get("/health", response_model=schemas.Health, status_code=status.HTTP_200_OK)
def check_health():
    return schemas.Health(status=schemas.HealthStatus.ready)


@app.post(
    "/",
    response_model=Union[schemas.Customer, schemas.Error],
    status_code=status.HTTP_200_OK,
)
def add_pet(
    customer: schemas.Customer, db: Session = Depends(db_session)
) -> schemas.Customer:
    if customer.id is not None:
        return schemas.Error(message="ID for new customers should not be specified")

    return crud.create_customer(db, customer=customer)


FastAPIInstrumentor.instrument_app(app)
