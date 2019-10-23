-- show tables from lahman2019clean;
show tables;
SHOW KEYS FROM lahman2019clean.appearances WHERE Key_name='PRIMARY';
SHOW INDEX FROM lahman2019clean.appearances WHERE Key_name='PRIMARY';
-- SELECT Column_name FROM (SHOW KEYS FROM lahman2019clean.appearances WHERE Key_name='PRIMARY');
SELECT * FROM information_schema.tables;
SELECT * FROM information_schema.key_column_usage;
-- Got the gist of the idea from https://dataedo.com/kb/query/mysql/list-all-primary-keys-and-their-columns
SELECT COLUMN_NAME FROM information_schema.key_column_usage WHERE CONSTRAINT_NAME='PRIMARY' AND TABLE_SCHEMA='lahman2019clean' AND TABLE_NAME='appearances';
SELECT * from lahman2019clean.appearances;
select count(*) from lahman2019clean.appearances;
SELECT COLUMN_NAME FROM information_schema.key_column_usage WHERE CONSTRAINT_NAME='PRIMARY' AND TABLE_SCHEMA='lahman2019clean' AND TABLE_NAME='batting';