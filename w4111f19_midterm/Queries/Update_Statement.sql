use classicmodels;
drop table if exists orders_copy;
create table orders_copy as select * from orders;

-- Test query
select * from orders_copy join orderdetails using(orderNumber) where orderNumber=10100;

select
	customers.customerNumber, customers.country, orders_copy.orderNumber, orders_copy.status from
    customers join orders_copy
    using (customerNumber)
    where country = 'Australia'
order by status;

/*Let's try this*/
SET SQL_SAFE_UPDATES=0;
UPDATE orders_copy
SET status='EMBARGOED'
WHERE (status!='Shipped' AND status!='Cancelled') AND customerNumber IN (
	SELECT customerNumber
    FROM customers 
    WHERE country='Australia');
SET SQL_SAFE_UPDATES=1;


-- Temp. JN was acting up (acually I think it was my eternal drive), so I had to store this somewhere.

%%sql
USE classicmodels;
SET SQL_SAFE_UPDATES=0;
UPDATE orders_copy
SET status='EMBARGOED'
WHERE (status!='Shipped' AND status!='Cancelled') AND customerNumber IN (
	SELECT customerNumber
    FROM customers 
    WHERE country='Australia');
SET SQL_SAFE_UPDATES=1;

select
	customers.customerNumber, customers.country, orders_copy.orderNumber, orders_copy.status from
    customers join orders_copy
    using (customerNumber)
    where country = 'Australia'
order by status;

