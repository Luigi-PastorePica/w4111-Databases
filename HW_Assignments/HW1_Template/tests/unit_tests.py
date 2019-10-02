# I write and test methods one at a time.
# This file contains unit tests of individual methods.

from HW_Assignments.HW1_Template.src.CSVDataTable import CSVDataTable
import logging
import os
import json


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

    print("Query result (regular) = \n", json.dumps(res, indent=2))

    # Providing no keys should return the same as the regular query above
    csv_tbl_no_keys = CSVDataTable("no_keys", connect_info, empty_key_cols)

    res = csv_tbl_no_keys.find_by_template(template=tmp, field_list=fields)

    print("Query result (no keys) = \n", json.dumps(res, indent=2))

    # Providing an empty set of fields should return an empty row for each row matched in the regular query above
    csv_tbl_no_fields = CSVDataTable("batting", connect_info, key_columns=key_cols)

    res = csv_tbl_no_fields.find_by_template(template=tmp, field_list=empty_fields)

    print("Query result (empty fields list) = \n", json.dumps(res, indent=2))

    # Providing no fields should return the fields in all columns for each row matched in the regular query above
    csv_tbl_no_fields = CSVDataTable("batting", connect_info, key_columns=key_cols)

    res = csv_tbl_no_fields.find_by_template(template=tmp)

    print("Query result (no field list provided) = \n", json.dumps(res, indent=2))

    # Providing an empty template should return all of the rows in the table
    csv_tbl_no_template = CSVDataTable("batting", connect_info, key_columns=key_cols)

    res = csv_tbl_no_template.find_by_template(template=empty_tmp, field_list=fields)

    res_last_elem = len(res) - 1
    print("Query result (no template) = \n", json.dumps(res[0:rows_to_show], indent=2), "\n\n***\n***\n***\n\n",
          json.dumps(res[res_last_elem - rows_to_show:res_last_elem], indent=2))


def t_find_by_key():

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

    print("Query result (single key) = \n", json.dumps(res, indent=2))

    # A proper key set is unique
    csv_tbl = CSVDataTable("player_multi", connect_info, key_columns=key_cols_multi)

    res = csv_tbl.find_by_primary_key(keys_multi, fields)

    print("Query result (multi-field key) = \n", json.dumps(res, indent=2))

    # This improper "key" should produce an exception, since it will return multiple results (i.e. not a proper key)
    csv_tbl = CSVDataTable("player_wrong_key", connect_info, key_columns=key_cols_wrong)

    try:
        res = csv_tbl.find_by_primary_key(keys_wrong, fields)
    except LookupError as tooMany:
        print("Exception caught")
        print("Query result (wrongly chosen key(s)) = \n{}".format(str(tooMany)))
    else:
        # Consider using an Assertion instead
        print("There should have been a LookupError. Result = ", json.dumps(res, indent=2))
        print("TEST FAILED!")

    # This query should return None, since the intended key value does not exist
    csv_tbl = CSVDataTable("player_no_match", connect_info, key_columns=key_cols_no_match)

    res = csv_tbl.find_by_primary_key(keys_no_match, fields)

    print("Query result (key without match) = \n", json.dumps(res, indent=2))


t_load()
t_find_by_template()
t_find_by_key()
