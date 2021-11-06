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

from typing import List
from fastapi import Depends, FastAPI, Query, status
from sqlalchemy.orm import Session
from data.database import engine, models, SessionLocal
from data import schemas
from . import crud

models.Base.metadata.create_all(bind=engine)


app = FastAPI(root_path="/pets")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health", status_code=status.HTTP_200_OK)
def check_health():
    return {"status": "Ready"}


@app.get("/catalog", response_model=List[schemas.Pet], status_code=status.HTTP_200_OK)
def get_pets_catalog(
    limit: int = Query(default=100, lte=100),
    offset: int = 0,
    db: Session = Depends(get_db),
) -> List[models.Pet]:
    ret = crud.get_available_pets(db, limit, offset)
    return ret


@app.post("/", response_model=schemas.Pet, status_code=status.HTTP_200_OK)
def add_pet(pet: schemas.Pet, db: Session = Depends(get_db)) -> models.Pet:
    return crud.create_pet(db, pet=pet)
