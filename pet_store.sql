DROP DATABASE IF EXISTS pet_store;
CREATE DATABASE pet_store;

USE pet_store;

CREATE TABLE pets (
    id INT UNSIGNED AUTO_INCREMENT,
    display_name VARCHAR(255) NOT NULL,
    current_price INT UNSIGNED NOT NULL,
    available_amount INT UNSIGNED NOT DEFAULT 0,

    CONSTRAINT pk_id PRIMARY KEY (id),
    CONSTRAINT uc_display_name UNIQUE (display_name)
);

CREATE TABLE customers (
    id INT UNSIGNED AUTO_INCREMENT,
    delivery_address VARCHAR(255) NOT NULL,
    contact_number VARCHAR(255) NOT NULL,

    CONSTRAINT pk_id PRIMARY KEY (id)
);

CREATE TABLE order_items (
    id INT UNSIGNED AUTO_INCREMENT,
    pet_id INT NOT NULL,
    order_id INT NOT NULL,
    amount INT NOT NULL,
    unit_price INT NOT NULL,

    CONSTRAINT pk_id PRIMARY KEY (id),
    CONSTRAINT fk_pet_id FOREIGN KEY (pet_id) REFERENCES pets(id),
    CONSTRAINT fk_order_id FOREIGN KEY (order_id) REFERENCES orders(id)
);

CREATE TABLE orders (
    id INT UNSIGNED AUTO_INCREMENT,
    customer_id INT NOT NULL,
    invoice_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    payment_timestamp TIMESTAMP NOT NULL,

    CONSTRAINT pk_id PRIMARY KEY (id),
    CONSTRAINT fk_customer_id FOREIGN KEY (customer_id) REFERENCES customers(id)
);
