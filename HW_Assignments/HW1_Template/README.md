# W4111_F19_HW1
Implementation template for homework 1.

## How CSVDataTable works:

- The methods ending in _by_template(template, ...) iterate over the entirety of the list self._rows looking to match the 
pattern given in their respective template argument. In turn, the matching in each iteration is done by the method 
matches_template(row, template) 

- matches_template(row, template), where row and template are dictionaries, iterates over the elements of row looking for 
key-value matches with template.

- The methods ending in _by_primary_key(key_fields, ...) and _by_key(key_fields, ...) internally use their _by_template 
counterparts for matching. The _generate_template(key_fields) method returns a template that can then be used as an 
argument for the corresponding _by_template method. 

- _generate_template(key_fields) uses the key_fields argument (a list of key values) and the CSVDataTable object's 
instance variable self.data.key_columns (a list of the columns that comprise the primary key for the table) to generate 
a dictionary. The dictionary generated is returned and it can be used as a template for a query. While there is no 
provided way to check the formatting of key_fields is correct, the function _check_key_fields_length(key_fields) checks 
that the length of key_fields matches the length of self.data.key_columns and raises a ValueError in case the do not 
match; in this way at least length mismatches can be easily identified. 

- insert(new_record), where new_record is a dictionary containing the key-value pairings for all the columns of 
self._rows. The values can be '' (empty strings). This method simply appends the dictionary to the end of the list 
self._rows. Then, it reorders the list based on the table's first column. Please note that **trying to insert a record 
with a primary key (key_columns) that is already present in the table will not work**. The method will print a warning 
and the new record will be discarded.

- _validate_template_and_fields(template, field_list) validates its arguments. The method creates a set containing all 
column names of the CSVDataTable instance. Then, it also creates independent sets for the elements in template.keys() 
and field_list. After that, it checks whether the smaller sets are a subset of the one containing all the columns of the 
instance. This method is used in all _by_template methods to avoid the confusion that could be caused by potentially 
more obscure errors raised by underlying modules. Code for this method was provided by Dr. Donal Ferguson (see notes 
below)

_check_for_duplicates(new_record) checks the entire table in the calling CSVDataTable instance for primary key 
duplicates.

### Notes on CSVDataTable.py:

insert() is highly inefficient at this point. It currently has to copy the entire contents of self._rows in 
order to sort the table.

_check_for_duplicates() is only used in insert(). Because of the current implementation of the class (no indexing), 
using this method in _load() or add_rows() would be highly inefficient. Therefore, it is assumed that the CSV file being 
imported into the CSVDataTable instance has no primary key (key_columns) duplicates.

find_by_template() looks a bit messy. I have left in the code a different, commented-out version of the function. This 
alternate version does not work properly for an unknown reason; however, I left it because if it is made to work, I 
think the code will be cleaner, more understandable and more maintainable.

The idea of how to obtain the first element of an ordered dictionary comes from this post: 
https://stackoverflow.com/questions/30362391/how-do-you-find-the-first-key-in-a-dictionary

The idea to use operator.itemgetter() for sorting the self._rows list comes from this post:
https://www.geeksforgeeks.org/ways-sort-list-dictionaries-values-python-using-itemgetter/

The solution for properly representing a 1 row table using pandas.DataFrame comes from this post: 
https://stackoverflow.com/questions/42202872/how-to-convert-list-to-row-dataframe-with-pandas

_validate_template_and_fields() and its code were provided by Dr. Donald Ferguson in the Columbia CVN video 
video_oh18sep_2019

## How RDBDataTable works:

Most methods in this class depend on dbutils. dbutils is in charge of translating structures and data from the format 
used by the API common to CSVDataTable and RDBDataTable to the appropriate sql format. 

The _by_key methods are dependent on the _by_template methods. This is because the _by_key methods use 
_generate_template() to create a template that can then be used as arguments for the _by_template methods.

### Notes on RDBDataTable.py:


---

## Unit Tests: 

###On TestTable.csv

Path: HW_Assignments/HW1_Template/tests/csv_files/TestTable.csv

You will notice **only some** of the tests are performed on TestTable.csv. This is mainly because of two reasons:
1. The idea of creating a table that contains a small subset of rows from another table came late in development.
2. Test table TestTable.csv was created with the objective of inserting, updating and deleting data from a table without
modifying the original tables in Data/Baseball folder. Therefore, changing other tests (like find_by_) to use TestTable, 
which implies changing search templates, keys, values, etc. would have meant an unnecessary time investment for the 
purpose of the assignment and of the tests.

###How csv_table_tests works

Path: HW_Assignments/HW1_Template/tests/csv_table_tests.py  
Output: HW_Assignments/HW1_Template/tests/logs/csv_table_test.txt

Tests for:

- t_find_by_primary_key
- t_find_by_template
- t_delete_by_key
- t_delete_by_template
- t_update_by_key
- t_update_by_template
- t_insert

Perform their operations on the copy of the CSV files temporarily held in memory when the program runs. As a result, no 
changes are made to the original data table files.

The test for:

- t_save

Saves the CSV table currently in memory into the data table (csv file) opened by the CSVDataTable object. 

### Notes for csv_table_tests.py

For the purpose of reducing time for iterations in the development of tests, a smaller test table has been created in a 
CSV file called TestTable.csv, which is expected to be in the __tests__ directory. If the table does not exist, t_save 
will create it and fill it with a reduced version of an already existing table. In this particular case, TestTable.csv 
contains 1 out of every 10 records in People.csv.

**Very Important:**

If the table TestTable.csv exists, but it is empty, the program will produce an error. To prevent this error, there are 
three options:
1. Place csv formatted content in TestTable.csv
2. Rename a copy of another csv formatted file to TestTable.csv (analogous to option 1)
3. Remove (delete) TestTable.csv from the tests directory. When t_save is run again, it will then create a new 
TestTable.csv file.

###How rdb_table_tests works

All methods perform their operations on tables stored in a MySQL database. An RDBDataTable object is instantiated 
inside each of the tests. This is done because the connection information might differ slightly from test to test.


### Notes for rdb_table_tests.py
Path: HW_Assignments/HW1_Template/tests/rdb_table_tests.py  
Output: HW_Assignments/HW1_Template/tests/logs/rdb_table_test.txt

t_update_by_template has part of the test in a try block. This was done because the block in question is trying to make 
an update to the table without providing the primary key in the template. Apparently, MySQL could complain in certain 
cases when doing this particular kind of update. This error was thrown by MySQLWorkbench, which claimed the reason was 
that the DB is using safe update mode and thus cannot update without the primary key provided in the template. However, 
pymysql did not raise the same warning and was more than happy to oblige and just proceeded to make the update. Because 
of this, it is unclear at the moment whether pymsql can throw an error when trying to perform this statement under 
certain conditions. Until then, the test will catch any exception that is thrown when performing that particular update.