-- Copyright (c) 2021, Nadun De Silva. All Rights Reserved.
--
-- Licensed under the Apache License, Version 2.0 (the "License");
-- you may not use this file except in compliance with the License.
-- You may obtain a copy of the License at
--
--   http://www.apache.org/licenses/LICENSE-2.0
--
-- Unless required by applicable law or agreed to in writing, software
-- distributed under the License is distributed on an "AS IS" BASIS,
-- WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
-- See the License for the specific language governing permissions and
-- limitations under the License.

DROP DATABASE IF EXISTS pet_store;
CREATE DATABASE pet_store;

USE pet_store;

CREATE TABLE pets (
    id INT UNSIGNED AUTO_INCREMENT,
    display_name VARCHAR(255) NOT NULL,
    kind VARCHAR(255) NOT NULL,
    current_price DECIMAL(13, 4) UNSIGNED NOT NULL,
    available_amount INT UNSIGNED NOT NULL DEFAULT 0,

    CONSTRAINT pk_id PRIMARY KEY (id),
    CONSTRAINT uc_display_name UNIQUE (display_name)
);

CREATE TABLE customers (
    id INT UNSIGNED AUTO_INCREMENT,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    delivery_address VARCHAR(255) NOT NULL,
    contact_number VARCHAR(255) NOT NULL,

    CONSTRAINT pk_id PRIMARY KEY (id)
);

CREATE TABLE orders (
    id INT UNSIGNED AUTO_INCREMENT,
    customer_id INT UNSIGNED NOT NULL,
    creation_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    payment_timestamp TIMESTAMP,

    CONSTRAINT pk_id PRIMARY KEY (id),
    CONSTRAINT fk_customer_id FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE TABLE order_items (
    id INT UNSIGNED AUTO_INCREMENT,
    pet_id INT UNSIGNED NOT NULL,
    order_id INT UNSIGNED NOT NULL,
    amount INT NOT NULL,
    unit_price DECIMAL(13, 4) NOT NULL,

    CONSTRAINT pk_id PRIMARY KEY (id),
    CONSTRAINT fk_pet_id FOREIGN KEY (pet_id) REFERENCES pets(id),
    CONSTRAINT fk_order_id FOREIGN KEY (order_id) REFERENCES orders(id)
);
