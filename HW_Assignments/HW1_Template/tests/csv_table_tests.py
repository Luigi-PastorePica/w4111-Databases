"""
Programmer: Luigi A. Pastore Pica
UNI: lap2204
Template code provided by Donald F. Ferguson, Ph.D.

This file contains unit tests of individual methods in CSVDataTable.

The code is very similar, but not identical, to unit_tests.py. Going forward, please use this test instead as all
future development of unit tests for CSVDataTable will be made on this document.
"""


from HW_Assignments.HW1_Template.src.CSVDataTable import CSVDataTable
import logging
import os
import csv
import pandas as pd
from collections import OrderedDict as OrderedDict

# Using pandas will make the output more readable.
pd.set_option("display.width", 256)
pd.set_option('display.max_columns', 20)


# The logging level to use should be an environment variable, not hard coded.
logging.basicConfig(level=logging.DEBUG)

# Also, the 'name' of the logger to use should be an environment variable.
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# This should also be an environment variable.
# Also not the using '/' is OS dependent, and windows might need `\\`
data_dir = os.path.abspath("../Data/Baseball")


def t_load():

    connect_info = {
        "directory": data_dir,
        "file_name": "People.csv"
    }

    csv_tbl = CSVDataTable("people", connect_info, None)

    print("Created table = " + str(csv_tbl))


def t_find_by_template():

    rows_to_show = 3

    connect_info = {
        "directory": data_dir,
        "file_name": "Batting.csv"
    }
    key_cols = ['playerID', 'teamID', 'yearID', 'stint']
    fields = ['playerID', 'teamID', 'yearID', 'AB', 'H', 'HR', 'RBI']
    tmp = {'teamID': 'BOS', 'yearID': '1960'}

    empty_key_cols = []
    empty_fields = []
    empty_tmp = {}

    # Should return the results of SELECT <fields> FROM Batting.csv WHERE <tmp template>
    csv_tbl = CSVDataTable("batting", connect_info, key_columns=key_cols)

    res = csv_tbl.find_by_template(template=tmp, field_list=fields)

    print("Query result (regular) = \n", pd.DataFrame(res))

    # Providing no keys should return the same as the regular query above
    csv_tbl_no_keys = CSVDataTable("no_keys", connect_info, empty_key_cols)

    res = csv_tbl_no_keys.find_by_template(template=tmp, field_list=fields)

    print("Query result (no keys) = \n", pd.DataFrame(res))

    # Providing an empty set of fields should return a full row for each row matched in the regular query above
    csv_tbl_no_fields = CSVDataTable("batting", connect_info, key_columns=key_cols)

    res = csv_tbl_no_fields.find_by_template(template=tmp, field_list=empty_fields)

    print("Query result (empty fields list) = \n", pd.DataFrame(res))

    # Providing no fields should return the fields in all columns for each row matched in the regular query above
    csv_tbl_no_fields = CSVDataTable("batting", connect_info, key_columns=key_cols)

    res = csv_tbl_no_fields.find_by_template(template=tmp)

    print("Query result (no field list provided) = \n", pd.DataFrame(res))

    # Providing an empty template should return all of the rows in the table
    csv_tbl_no_template = CSVDataTable("batting", connect_info, key_columns=key_cols)

    res = csv_tbl_no_template.find_by_template(template=empty_tmp, field_list=fields)

    res_last_elem = len(res) - 1
    pre_second_to_last_index = res_last_elem - rows_to_show
    print("Query result (no template) = \n", pd.DataFrame(res[0:rows_to_show], index=range(1, rows_to_show + 1)),
          "\n\n***\n***\n***\n\n",
          pd.DataFrame(res[pre_second_to_last_index:len(res)], index=range(pre_second_to_last_index + 1, len(res) + 1)))


def t_find_by_primary_key():

    connect_info = {
        "directory": data_dir,
        "file_name": "People.csv"
    }

    key_cols_single = ['playerID']
    keys_single = ['willite01']

    key_cols_multi = ['nameGiven', 'retroID', 'bbrefID']
    keys_multi = ['Theodore Samuel', 'willt103', 'willite01']

    key_cols_wrong = ['birthState', 'nameLast']
    keys_wrong = ['CA', 'Williams']

    key_cols_no_match = ['nameGiven']
    keys_no_match = ['Ted Williams']

    fields = ['playerID', 'retroID', 'bbrefID', 'nameFirst', 'nameLast', 'nameGiven']

    # A proper key is unique
    csv_tbl = CSVDataTable("player", connect_info, key_columns=key_cols_single)

    res = csv_tbl.find_by_primary_key(keys_single, fields)

    print("Query result (single key) = \n", pd.DataFrame([res]))

    # A proper key set is unique
    csv_tbl = CSVDataTable("player_multi", connect_info, key_columns=key_cols_multi)

    res = csv_tbl.find_by_primary_key(keys_multi, fields)

    print("Query result (multi-field key) = \n", pd.DataFrame([res]))

    # This improper "key" should produce an exception, since it will return multiple results (i.e. not a proper key)
    csv_tbl = CSVDataTable("player_wrong_key", connect_info, key_columns=key_cols_wrong)

    try:
        res = csv_tbl.find_by_primary_key(keys_wrong, fields)
    except LookupError as tooMany:
        print("Exception caught")
        print("Query result (wrongly chosen key(s)) = \n{}".format(str(tooMany)))
    else:
        # Consider using an Assertion instead
        print("There should have been a LookupError. Result = ", pd.DataFrame(res))
        print("TEST FAILED!")

    # This query should return None, since the intended key value does not exist
    csv_tbl = CSVDataTable("player_no_match", connect_info, key_columns=key_cols_no_match)

    res = csv_tbl.find_by_primary_key(keys_no_match, fields)

    print("Query result (key without match) = \n", pd.DataFrame([res]))


def t_delete_by_template():

    connect_info = {
        "directory": data_dir,
        "file_name": "Batting.csv"
    }

    key_cols = ['playerID', 'teamID', 'yearID', 'stint']
    fields = ['playerID', 'teamID', 'yearID']
    tmp = {'teamID': 'BOS', 'yearID': '1960'}

    # should there be an add before calling the delete?
    # maybe there should. That way I can control how many rows there are with a certain template.

    csv_tbl = CSVDataTable("trimmed table", connect_info, key_cols)
    rows_deleted = csv_tbl.delete_by_template(tmp)
    print("Rows deleted = ", rows_deleted)  # Use assertion

    res = csv_tbl.find_by_template(tmp, fields)
    print("Query result using the same template should be empty: \n", pd.DataFrame([res]))  # Again, use assertion


def t_delete_by_key():

    connect_info = {
        "directory": data_dir,
        "file_name": "People.csv"
    }

    key_cols = ['nameGiven', 'retroID', 'bbrefID']
    key_fields = ['Theodore Samuel', 'willt103', 'willite01']

    csv_tbl = CSVDataTable("trimmed table", connect_info, key_columns=key_cols)

    rows_deleted = csv_tbl.delete_by_key(key_fields)

    print("Rows deleted = ", rows_deleted)  # Use assertion

    res = csv_tbl.find_by_primary_key(key_fields)

    print("Query result using the same key should be empty: \n", pd.DataFrame([res]))  # Again, use assert


def t_update_by_template():

    connect_info = {
        "directory": data_dir,
        "file_name": "Batting.csv"
    }

    key_cols = ['playerID', 'teamID', 'yearID', 'stint']
    new_vals = {'teamID': 'BOS1', 'IBB': '0', 'HBP': '0', 'SH': '0', 'SF': '0'}
    tmp_old = {'teamID': 'BOS', 'yearID': '1960'}
    tmp_new = {'teamID': 'BOS1', 'yearID': '1960'}

    csv_tbl = CSVDataTable("updated table", connect_info, key_cols)

    rows_updated = csv_tbl.update_by_template(tmp_old, new_vals)

    print("Rows updated = ", rows_updated)  # Use assertion

    res = csv_tbl.find_by_template(tmp_old)

    print("Query result with old template should be empty: \n", pd.DataFrame([res]))  # Again, use assertion

    res = csv_tbl.find_by_template(tmp_new)

    print("Query result with new template: \n", pd.DataFrame(res))  # Again, use assertion


def t_update_by_key():

    connect_info = {
        "directory": data_dir,
        "file_name": "People.csv"
    }

    key_cols = ['nameGiven', 'retroID', 'bbrefID']
    new_vals = {'nameGiven': 'Theodore S.', 'weight': '204'}
    key_fields = ['Theodore Samuel', 'willt103', 'willite01']
    new_key_fields = ['Theodore S.', 'willt103', 'willite01']

    csv_tbl = CSVDataTable("trimmed table", connect_info, key_cols)

    res = csv_tbl.find_by_primary_key(key_fields)

    print("Query result: \n", pd.DataFrame([res]))  # Again, use assert

    rows_updated = csv_tbl.update_by_key(key_fields, new_vals)

    print("Rows updated = ", rows_updated)  # Use assertion

    res = csv_tbl.find_by_primary_key(key_fields)

    print("Query result using old values should be empty: \n", pd.DataFrame([res]))  # Again, use assert

    res = csv_tbl.find_by_primary_key(new_key_fields)

    print("Query result using new values {}: \n".format(new_vals), pd.DataFrame([res]))  # Again, use assert


def t_insert():

    connect_info = {
        "directory": data_dir,
        "file_name": "People.csv"
    }

    key_cols = ['nameGiven', 'retroID', 'bbrefID']
    key_fields = ['Bilba Labingi', 'midget01', 'baggbil01']
    new_record = {'playerID': 'baggbil01', 'birthYear': '2900', 'birthMonth': '01', 'birthDay': '02',
                  'birthCountry': 'Arnor', 'birthState': 'The Shire', 'birthCity': 'Hobbiton',
                  'deathYear': '', 'deathMonth': '', 'deathDay': '',
                  'deathCountry': 'Aman', 'deathState': '', 'deathCity': '',
                  'nameFirst': 'Bilbo', 'nameLast': 'Baggins', 'nameGiven': 'Bilba Labingi',
                  'weight': 'not much', 'height': 'very short', 'bats': '', 'throws': '',
                  'debut': '', 'finalGame': '',
                  'retroID': 'midget01', 'bbrefID': 'baggbil01'}

    csv_tbl = CSVDataTable("Expanded table", connect_info, key_columns=key_cols)

    csv_tbl.insert(new_record)

    # insert() should warn about the key being a duplicate and prevent insertion
    csv_tbl.insert(new_record)

    # Checks that the row was properly inserted in the self._rows instance variable.
    # In addition, if a duplicate was inserted, find_by_primary_key() would raise a LookupError.
    res = csv_tbl.find_by_primary_key(key_fields)

    print("Row inserted = \n", pd.DataFrame([res], columns=res.keys()))  # Use assertion


def t_save():

    connect_info = {
        "directory": data_dir,
        "file_name": "People.csv"
    }

    connect_info_test = {
        "directory": "./csv_files",
        "file_name": "TestTable.csv"
    }

    key_cols = ['nameGiven', 'retroID', 'bbrefID']

    dir_info = connect_info.get("directory")
    file_n = connect_info.get("file_name")
    full_name = os.path.join(dir_info, file_n)

    dir_info_test = connect_info_test.get("directory")
    file_n_test = connect_info_test.get("file_name")
    full_name_test = os.path.join(dir_info_test, file_n_test)

    truncate_step = 10
    truncate_counter = 0
    truncated_table = []

    # If the CSV file at full_name_test does not exist, this will create it based on the CSV file at full_name
    if not (os.path.exists(full_name_test) and os.path.isfile(full_name_test)):

        with open(full_name, "r") as original_file:
            csv_d_rdr = csv.DictReader(original_file)
            for row in csv_d_rdr:
                if (truncate_counter % truncate_step) == 0:
                    truncated_table.append(row)
                truncate_counter += 1

        with open(full_name_test, "w") as csv_file:
            field_list = csv_d_rdr.fieldnames
            csv_d_writer = csv.DictWriter(csv_file, fieldnames=field_list)
            csv_d_writer.writeheader()
            for row in truncated_table:
                csv_d_writer.writerow(row)

    csv_tbl = CSVDataTable("Test table", connect_info_test, key_columns=key_cols)

    statinfo = os.stat(full_name_test)
    last_modified_prev = statinfo.st_mtime

    csv_tbl.save()

    statinfo = os.stat(full_name_test)
    last_modified_post= statinfo.st_mtime

    # This probably should go in CSVDataTable.save() instead. If so, it should throw an exception.
    # The exception can then be used here as some kind of trigger for an assert
    if last_modified_post > last_modified_prev:
        print("Saved changes in {}".format(full_name_test))
    else:
        print("The changes might not have been saved.")


t_load()
t_find_by_template()
t_find_by_primary_key()
t_delete_by_template()
t_delete_by_key()
t_update_by_template()
t_update_by_key()
t_insert()
t_save()

print("\n-------END OF UNIT TESTS -------\n")