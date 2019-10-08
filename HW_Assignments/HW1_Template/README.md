# W4111_F19_HW1
Implementation template for homework 1.

How CSVDataTable works:

The methods ending in _by_template(template, ...) iterate over the entirety of the list self._rows looking to match the 
pattern given in their respective template argument. In turn, the matching in each iteration is done by the method 
matches_template(row, template) 

matches_template(row, template), where row and template are dictionaries, iterates over the elements of row looking for 
key-value matches with template.

The methods ending in _by_primary_key(key_fields, ...) and _by_key(key_fields, ...) internally use their _by_template 
counterparts for matching. The _generate_template(key_fields) method returns a template that can then be used as an 
argument for the corresponding _by_template method. 

_generate_template(key_fields) uses the key_fields argument (a list of key values) and the CSVDataTable object's 
instance variable self.data.key_columns (a list of the columns that comprise the primary key for the table) to generate 
a dictionary. The dictionary generated is returned and it can be used as a template for a query. While there is no 
provided way to check the formatting of key_fields is correct, the function _check_key_fields_length(key_fields) checks 
that the length of key_fields matches the length of self.data.key_columns and raises a ValueError in case the do not 
match; in this way at least length mismatches can be easily identified. 

CSVDataTable.insert(new_record), where new_record is a dictionary containing the key-value pairings for all the columns 
of self._rows. The values can be '' (empty strings). This method simply appends the dictionary to the end of the list 
self._rows. Then, it reorders the list based on the table's first column.

The idea of how to obtain the first element of an ordered dictionary comes from this post: 
https://stackoverflow.com/questions/30362391/how-do-you-find-the-first-key-in-a-dictionary

The idea to use operator.itemgetter() for sorting the self._rows list comes from this post:
https://www.geeksforgeeks.org/ways-sort-list-dictionaries-values-python-using-itemgetter/

Note that CSVDataTable.insert() is highly inefficient at this point. It currently has to copy the entire contents of 
self._rows in order to sort the table.

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

Perform their operations on the copy of the CSV files temporarily held in memory when the program runs. As a result, no 
changes are made to the original data table files.

The test for:

t_save

saves the CSV table currently in memory into the data table (csv file) opened by the CSVDataTable object. For this 
purpose, a smaller test table has been created in a CSV file called Csv_test.csv. 

