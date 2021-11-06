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

from fastapi import Depends, FastAPI, status
from sqlalchemy.orm import Session
from data.database import db_session
from data import schemas
from . import crud

app = FastAPI(root_path="/customers")


@app.get("/health", status_code=status.HTTP_200_OK)
def check_health():
    return {"status": "Ready"}


@app.post("/", response_model=schemas.Customer, status_code=status.HTTP_200_OK)
def add_pet(
    customer: schemas.Customer, db: Session = Depends(db_session)
) -> schemas.Customer:
    if customer.id is not None:
        raise Exception("ID for new customers should not be specified")
    if len(customer.contact_number) != 12:
        raise Exception(
            "Invalid length of contact number of customer; expected 12, but received "
            + str(len(customer.contact_number))
        )
    return crud.create_customer(db, customer=customer)
