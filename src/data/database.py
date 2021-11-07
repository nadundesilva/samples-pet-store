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

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

__DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")

__connect_args = {}
if __DATABASE_URL.startswith("sqlite://"):
    __connect_args["check_same_thread"] = False

__engine = create_engine(__DATABASE_URL, connect_args=__connect_args)
__SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=__engine)

Base = declarative_base()
Base.metadata.create_all(bind=__engine)


def db_session():
    db = __SessionLocal()
    try:
        yield db
    finally:
        db.close()
