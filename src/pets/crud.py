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
from sqlalchemy.orm import Session
from . import db_models as models
from data import schemas


def get_available_pets(db: Session, limit: int, offset: int) -> List[schemas.Pet]:
    db_pets = (
        db.query(models.Pet)
        .filter(models.Pet.available_amount > 0)
        .limit(limit)
        .offset(offset)
        .all()
    )
    return [schemas.Pet(**db_pet.__dict__) for db_pet in db_pets]


def create_pet(db: Session, pet: schemas.Pet) -> schemas.Pet:
    db_pet = models.Pet(
        display_name=pet.display_name,
        kind=pet.kind,
        current_price=pet.current_price,
        available_amount=pet.available_amount,
    )
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    return schemas.Pet(**db_pet.__dict__)
