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

    print("Query result (no fields) = \n", json.dumps(res, indent=2))

    # Providing an empty template should return all of the rows in the table
    csv_tbl_no_template = CSVDataTable("batting", connect_info, key_columns=key_cols)

    res = csv_tbl_no_template.find_by_template(template=empty_tmp, field_list=fields)

    print("Query result (no template) = \n", json.dumps(res, indent=2))
    
def t_delete_by_template()
    
    # should there be an add before calling the delete?
    # maybe there should. That way I can control how many rows there are with a certain template.
    tmp = {'teamID': 'BOS', 'yearID': '1960'}
    deleted_rows = delete_by_template(tmp)
    print ("Rows deleted = ", deleted_rows)
    
t_load()
t_find_by_template()