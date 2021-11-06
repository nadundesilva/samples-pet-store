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

from sqlalchemy import Column, ForeignKey, Integer, String, Text, Time
from sqlalchemy.orm import relationship
from . import Base


class Pet(Base):
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True, index=True)
    display_name = Column(String)
    kind = Column(String)
    current_price = Column(Integer)
    available_amount = Column(Integer)


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    delivery_address = Column(Text)
    contact_number = Column(String)

    orders = relationship("Order", back_populates="customer")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    pet_id = Column(Integer, ForeignKey("pets.id"))
    order_id = Column(Integer, ForeignKey("orders.id"))
    amount = Column(Integer)
    unit_price = Column(Integer)

    order = relationship("Order", back_populates="items")
    pet = relationship("Pet")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    payment_timestamp = Column(Time)

    items = relationship("OrderItem", back_populates="order")
    customer = relationship("Customer", back_populates="orders")
