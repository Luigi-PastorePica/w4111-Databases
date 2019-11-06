USE classicmodels;
SELECT distinct status FROM orders;
SELECT * FROM orders WHERE status NOT IN (SELECT DISTINCT status FROM orders); -- Self referencing.
SELECT * FROM orders WHERE status is null;

ALTER TABLE orders_copy
CHANGE status status ENUM('Shipped', 'Resolved', 'Cancelled', 'On Hold', 'Disputed', 'In Process', 'EMBARGOED');

UPDATE orders_copy
SET status = 'Sent'
WHERE status = 'Shipped';

INSERT INTO orders_copy
(orderNumber, orderDate, requiredDate, status, customerNumber)
values(1111111111, '2040-01-01', '2040-01-02', 'coming', 103);

SELECT * FROM ORDERS_COPY;