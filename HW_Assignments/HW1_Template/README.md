# W4111_F19_HW1
Implementation template for homework 1.

Unit Tests: 

HW1_Template/tests/unit_tests.py

Tests for:

t_find_by_primary_key
t_find_by_template
t_delete_by_key
t_delete_by_template
t_update_by_key
t_update_by_template
t_insert

Perform their operations on the copy of the CSV files temporarily held in memory when the program runs. As a result, no changes are made to the original data table files.

The test for:

t_save

saves the CSV table currently in memory into the data table (csv file) opened by the CSVDataTable object. For this purpose, a smaller test table has been created in a CSV file called Csv_test.csv. 

