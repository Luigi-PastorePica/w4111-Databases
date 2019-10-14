"""
Programmer: Luigi A. Pastore Pica
UNI: lap2204
Template code provided by Donald F. Ferguson, Ph.D.

This file contains unit tests of individual methods in RDBDataTable.

"""


from HW_Assignments.HW1_Template.src.RDBDataTable import RDBDataTable
import HW_Assignments.HW1_Template.src.dbutils as dbutils

import pymysql
import json
import pandas as pd

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


# t_init() provided by Donald F. Ferguson, Ph.D.
# I made some modifications, thought they were unfruitful.
def t_init():
    c_info = {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "password": "dbuserdbuser",
        "db": "lahman2019raw",
        "cursorclass": pymysql.cursors.DictCursor
    }

    r_dbt = RDBDataTable("People", connect_info=c_info, key_columns=['playerID'])
    # TODO This print statement does not work.
    # print("RDB table = ", r_dbt)

# Maybe this code should go in a different test file. However, such tests are not required for the moment.
# t_template_to_where_clause() code was provided by Dr. Donald Ferguson.
# def t_template_to_where_clause():
#
#     table_name = "lahman2019raw.people"
#     fields = ['nameLast', 'nameFirst', 'birthYear', 'birthState', 'birthMonth']
#     template = { "nameLast": "Williams", "birthCity": "San Diego"}
#     sql, args = dbutils.create_select(table_name, template, fields)
#     sql_no_fields, args_no_fields = dbutils.create_select(table_name, template, fields=None)
#
#     print("SQL = ", sql, ", args = ", args)
#
#     c_info = {
#         "host": "localhost",
#         "port": 3306,
#         "user": "root",
#         "password": "dbuserdbuser",
#         "db": "lahman2019raw",
#         "cursorclass": pymysql.cursors.DictCursor
#     }
#
#     result = dbutils.run_q(sql, args, conn=dbutils.get_connection(c_info))
#     if result[1] is not None:
#         print("Full query:\n", pd.DataFrame(result[1]))
#     else:
#         print("None.")
#
#     result = dbutils.run_q(sql_no_fields, args_no_fields, conn=dbutils.get_connection(c_info))
#     if result[1] is not None:
#         print("No fields (SELECT *):\n", pd.DataFrame(result[1]))
#
#     else:
#         print("None.")


def t_find_by_primary_key():

    table_name = "lahman2019raw.people"
    fields = ['nameLast', 'nameFirst', 'birthYear', 'birthState', 'birthMonth']
    key_cols = ['playerID']
    key_fields = ['willite01']

    # print("SQL = ", sql, ", args = ", args)

    c_info = {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "password": "dbuserdbuser",
        "db": "lahman2019raw",
        "cursorclass": pymysql.cursors.DictCursor
    }

    rdb_table = RDBDataTable(table_name=table_name, connect_info=c_info, key_columns=key_cols)
    results, data = rdb_table.find_by_primary_key(key_fields=key_fields, field_list=fields)
    if results is not None:
        print("Full query:\nReturned {}\n".format(results), pd.DataFrame(data))
    else:
        print("No record found")

    results, data = rdb_table.find_by_primary_key(key_fields=key_fields)
    if results is not None:
        print("No fields (SELECT *):\nReturned {}\n".format(results), pd.DataFrame(data))
    else:
        print("No record found")


def t_find_by_template():

    table_name = "lahman2019raw.people"
    fields = ['nameLast', 'nameFirst', 'birthYear', 'birthState', 'birthMonth']
    template = {"nameLast": "Williams", "birthCity": "San Diego"}
    key_cols = ['playerID']

    # print("SQL = ", sql, ", args = ", args)

    c_info = {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "password": "dbuserdbuser",
        "db": "lahman2019raw",
        "cursorclass": pymysql.cursors.DictCursor
    }

    rdb_table = RDBDataTable(table_name=table_name, connect_info=c_info, key_columns=key_cols)
    results, data = rdb_table.find_by_template(template, fields)
    print("Full query:\nReturned {}\n".format(results), pd.DataFrame(data))
    results, data = rdb_table.find_by_template(template)
    print("No fields (SELECT *):\nReturned {}\n".format(results), pd.DataFrame(data))


def t_delete_by_key():

    table_name = "lahman2019raw.testtable"
    key_cols = ['playerID']
    key_fields = ['baggbil01']

    c_info = {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "password": "dbuserdbuser",
        "db": "lahman2019raw",
        "cursorclass": pymysql.cursors.DictCursor
    }

    rdb_table = RDBDataTable(table_name=table_name, connect_info=c_info, key_columns=key_cols)
    print(rdb_table.find_by_primary_key(key_fields))
    results = rdb_table.delete_by_key(key_fields)
    print("Delete returned {}\n".format(results))


def t_delete_by_template():

    table_name = "lahman2019raw.testtable"
    template = {"nameLast": "Baggins", "birthCity": "Hobbiton"}
    key_cols = ['playerID', 'teamID', 'yearID', 'stint']

    c_info = {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "password": "dbuserdbuser",
        "db": "lahman2019raw",
        "cursorclass": pymysql.cursors.DictCursor
    }

    rdb_table = RDBDataTable(table_name=table_name, connect_info=c_info, key_columns=key_cols)
    results = rdb_table.delete_by_template(template=template)
    print("Delete returned {}\n".format(results))


def t_update_by_key():
    table_name = "lahman2019raw.testtable"
    key_cols = ['playerID']
    key_fields = ['baggbil01']
    new_values = {'height': 'not so short', 'weight': 'got chubby after a while'}

    c_info = {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "password": "dbuserdbuser",
        "db": "lahman2019raw",
        "cursorclass": pymysql.cursors.DictCursor
    }

    rdb_table = RDBDataTable(table_name=table_name, connect_info=c_info, key_columns=key_cols)

    results = rdb_table.update_by_key(key_fields=key_fields, new_values=new_values)
    print("Update returned:\n Updated rows: {}\n".format(results))


def t_update_by_template():
    table_name = "lahman2019raw.testtable"
    template_wo_key = {"nameLast": "Baggins", "birthCity": "Hobbiton"}
    template_w_key = {"playerID": "baggbil01", "nameLast": "Baggins", "birthCity": "Hobbiton"}
    key_cols = ['playerID', 'teamID', 'yearID', 'stint']
    new_values1 = {'brithYear': 'c. 2900'}
    new_values2 = {'finalGame': 'Against Smaug'}

    c_info = {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "password": "dbuserdbuser",
        "db": "lahman2019raw",
        "cursorclass": pymysql.cursors.DictCursor
    }

    rdb_table = RDBDataTable(table_name=table_name, connect_info=c_info, key_columns=key_cols)

    # This block of code needs to be in a try-except block because MySQL could deny the update operation if a key is not
    # provided in the template. See README.md for more details.
    try:
        results = rdb_table.update_by_template(template=template_wo_key, new_values=new_values1)
        print("Update returned:\n Updated rows: {}\n".format(results))
    except Exception as e:
        print("Could not update because of DB error: {}".format(str(e)))

    results = rdb_table.update_by_template(template=template_w_key, new_values=new_values2)
    print("Update returned:\n Updated rows: {}\n".format(results))


def t_insert():

    table_name = "lahman2019raw.testtable"
    # fields = ['nameLast', 'nameFirst', 'birthYear', 'birthState', 'birthMonth']
    # template = {"nameLast": "Williams", "birthCity": "San Diego"}
    new_record = new_record = {'playerID': 'baggbil01', 'birthYear': '2900', 'birthMonth': '01', 'birthDay': '02',
                  'birthCountry': 'Arnor', 'birthState': 'The Shire', 'birthCity': 'Hobbiton',
                  'deathYear': '', 'deathMonth': '', 'deathDay': '',
                  'deathCountry': 'Aman', 'deathState': '', 'deathCity': '',
                  'nameFirst': 'Bilbo', 'nameLast': 'Baggins', 'nameGiven': 'Bilba Labingi',
                  'weight': 'not much', 'height': 'very short', 'bats': '', 'throws': '',
                  'debut': '', 'finalGame': '',
                  'retroID': 'midget01', 'bbrefID': 'baggbil01'}

    key_cols = ['playerID', 'teamID', 'yearID', 'stint']

    # print("SQL = ", sql, ", args = ", args)

    c_info = {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "password": "dbuserdbuser",
        "db": "lahman2019raw",
        "cursorclass": pymysql.cursors.DictCursor
    }

    rdb_table = RDBDataTable(table_name=table_name, connect_info=c_info, key_columns=key_cols)
    rdb_table.insert(new_record=new_record)

    results, data = rdb_table.find_by_template({'playerID': 'baggbil01'})

    if results > 0:
        print("Insert was successful.\nFound in table the following record: \n{}".format(pd.DataFrame(data)))
    else:
        print("Insert failed. The record could not be found after insert statement.")

    try:
        print("Attempting to insert record with duplicate primary key: ")
        rdb_table.insert(new_record=new_record)
    except pymysql.IntegrityError as ie:
        print("Duplicate insert denied successfully: {}".format(str(ie)))
        print("TEST PASSED!")
    else:
        print("Insert should have been stopped due to duplicate entry, but it was not.\n")
        print("TEST FAILED!")

    try:
        print("Attempting to insert new record with empty set of values:")
        rdb_table.insert(new_record={})
    except pymysql.InternalError as ie:
        print("Insert using empty set of values was not permitted: {}".format(str(ie)))
        print("TEST PASSED!")
    else:
        print("Insert should have been stopped due to empty set of values, but it was not.\n")
        print("TEST FAILED!")


def t_get_rows():

    table_name = "lahman2019raw.testtable"
    key_cols = ['playerID']

    c_info = {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "password": "dbuserdbuser",
        "db": "lahman2019raw",
        "cursorclass": pymysql.cursors.DictCursor
    }

    rdb_table = RDBDataTable(table_name=table_name, connect_info=c_info, key_columns=key_cols)
    results, data = rdb_table.get_rows()
    print("Getting all rows:\nRows: {}\n{}".format(results, pd.DataFrame(data)))


t_init()
# t_template_to_where_clause() # Test might go in another file in the future. Not needed right now.
t_find_by_primary_key()
t_delete_by_key()
t_find_by_template()
t_delete_by_template()
t_insert()
t_update_by_key()
t_update_by_template()
t_get_rows()
