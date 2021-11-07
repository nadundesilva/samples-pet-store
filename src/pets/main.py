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

from typing import List, Union
from fastapi import Depends, FastAPI, Query, status
from sqlalchemy.orm import Session
from data.database import db_session
from data import schemas
from . import crud

app = FastAPI(root_path="/pets")


@app.get("/health", response_model=schemas.Health, status_code=status.HTTP_200_OK)
def check_health():
    return {"status": "READY"}


@app.get("/", response_model=List[schemas.Pet], status_code=status.HTTP_200_OK)
def get_pets_catalog(
    limit: int = Query(default=100, lte=100),
    offset: int = 0,
    db: Session = Depends(db_session),
) -> List[schemas.Pet]:
    return crud.get_available_pets(db, limit, offset)


@app.patch(
    "/{pet_id}/reservation",
    response_model=schemas.Reservation,
    status_code=status.HTTP_200_OK,
)
def reserve_pet(
    pet_id: int, amount: int = Query(default=1, gt=0), db: Session = Depends(db_session)
) -> schemas.Pet:
    is_success, pet = crud.reserve_pet(db, pet_id, amount)
    return schemas.Reservation(
        status=("RESERVED" if is_success else "OUT_OF_STOCK"), pet=pet
    )


@app.post(
    "/",
    response_model=Union[schemas.Pet, schemas.Error],
    status_code=status.HTTP_200_OK,
)
def add_pet(pet: schemas.Pet, db: Session = Depends(db_session)) -> schemas.Pet:
    if pet.id is not None:
        return schemas.Error(message="ID for new pets should not be specified")
    return crud.create_pet(db, pet=pet)
