USE classicmodels;

select max(length(Name)) from countrycodes;

select name from countrycodes where length(name)=44;

select distinct count(code) from countrycodes;

ALTER TABLE countrycodes ORDER BY countryName;

select * from countrycodes ORDER BY countryName;

select * from customers_clean;

select count(distinct country) as number_of_countries from customers_clean;
select distinct count(country) as times, country from customers_clean group by country;

-- Commands in JN
SELECT * FROM classicmodels.countrycodes limit 10;
create table classicmodels.customers_clean as select * from classicmodels.customers;
select customerNumber, customerName, country from classicmodels.customers_clean limit 10;
--


-- Requirements:
-- Create country_code column from country column and append at right end of table
-- Remove country column
-- Implement Referential Integrity
	-- This, in part, means that we whould be able to execute the test python script in the notebook 
    -- and get an integrity error when trying to update the country code.
		-- try:
			-- 	%sql update customers_clean set country_code = 'XX' where customerNumber=103
			-- 	print("Getting here is bad.")
		-- 	except Exception as e:
			-- 	print("This is OK, e = ", e)
--

-- My Code
SET SQL_SAFE_UPDATES=0;
ALTER TABLE customers_clean 
ADD COLUMN countryCode VARCHAR(2),
ADD CONSTRAINT iso_country_code FOREIGN KEY (countryCode)
REFERENCES countrycodes (countryCode);

UPDATE customers_clean, countrycodes
SET customers_clean.countryCode = countrycodes.countryCode
WHERE country like CONCAT(countrycodes.countryName, '%') OR country like CONCAT(countrycodes.countryCode, '%');

UPDATE customers_clean
SET countryCode = 'GB'
WHERE country like 'U_K_' or country like 'UK' or country like 'United Kingdom';

ALTER TABLE customers_clean
CHANGE COLUMN countryCode countryCode VARCHAR(2) NOT NULL; -- Applying NN now because upon creation there were null values.

ALTER TABLE customers_clean
DROP COLUMN country;
SET SQL_SAFE_UPDATES=1;

--
-- Test
select * from customers_clean limit 10;
select * from customers_clean where countryCode is null;
select * from customers_clean where countryCode = 'GB';
select count(country) from customers_clean where country like 'UK%';
select distinct countryCode from customers_clean;
show create table customers_clean;