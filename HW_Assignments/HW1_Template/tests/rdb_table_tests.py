from HW_Assignments.HW1_Template.src.RDBDataTable import RDBDataTable
import HW_Assignments.HW1_Template.src.dbutils as dbutils

import pymysql
import json
import pandas as pd
import HW_Assignments.HW1_Template.src.dbutils

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


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


def t_template_to_where_clause():

    table_name = "lahman2019raw.people"
    fields = ['nameLast', 'nameFirst', 'birthYear', 'birthState', 'birthMonth']
    template = { "nameLast": "Williams", "birthCity": "San Diego"}
    sql, args = dbutils.create_select(table_name, template, fields)
    sql_no_fields, args_no_fields = dbutils.create_select(table_name, template, fields=None)

    print("SQL = ", sql, ", args = ", args)

    c_info = {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "password": "dbuserdbuser",
        "db": "lahman2019raw",
        "cursorclass": pymysql.cursors.DictCursor
    }

    result = dbutils.run_q(sql, args, conn=dbutils.get_connection(c_info))
    if result[1] is not None:
        print("Full query:\n", pd.DataFrame(result[1]))
    else:
        print("None.")

    result = dbutils.run_q(sql_no_fields, args_no_fields, conn=dbutils.get_connection(c_info))
    if result[1] is not None:
        print("No fields (SELECT *):\n", pd.DataFrame(result[1]))

    else:
        print("None.")


def t_find_by_template():

    table_name = "lahman2019raw.people"
    fields = ['nameLast', 'nameFirst', 'birthYear', 'birthState', 'birthMonth']
    template = {"nameLast": "Williams", "birthCity": "San Diego"}
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
    results, data = rdb_table.find_by_template(template, fields)
    print("Full query:\nReturned {}\n".format(results), pd.DataFrame(data))
    results, data = rdb_table.find_by_template(template)
    print("No fields (SELECT *):\nReturned {}\n".format(results), pd.DataFrame(data))


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
    results, data = rdb_table.insert(new_record=new_record)
    print("Insert returned:\nResults {}\n".format(results), pd.DataFrame(data))
    try:
        print("Attempting to insert record with duplicate primary key: ")
        results, data = rdb_table.insert(new_record=new_record)
    except pymysql.IntegrityError as ie:
        print("Duplicate insert denied successfully: {}".format(str(ie)))
    else:
        print("Insert should have been stopped due to duplicate entry.\n")
        print("Insert returned {}\n".format(results), pd.DataFrame(data))
        print("TEST FAILED!")

    try:
        print("Attempting to insert new record with empty set of values:")
        results, data = rdb_table.insert(new_record={})
    except pymysql.InternalError as ie:
        print("Insert using empty set of values was not permitted: {}".format(str(ie)))
    else:
        print("Insert should have been stopped due to empty set of values.\n")
        print("Inserting empty record returned {}\n".format(results), pd.DataFrame(data))
        print("TEST FAILED!")


def t_update_by_template():
    table_name = "lahman2019raw.testtable"
    template_wo_key = {"nameLast": "Baggins", "birthCity": "Hobbiton"}
    template_w_key = {"playerID": "baggbil01", "nameLast": "Baggins", "birthCity": "Hobbiton"}
    key_cols = ['playerID', 'teamID', 'yearID', 'stint']
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

    # These two try-except blocks are a hack to make the tests keep running.
    # TODO find how to confirm update took place and update the code below.
    try:
        print("Trying to update without specifying primary key value in WHERE")
        results, data = rdb_table.update_by_template(template=template_wo_key, new_values=new_values)
        print("Update returned {}\n".format(results), pd.DataFrame(data))
    except TypeError as te:
        print("Could not update: {}".format(str(te)))

    try:
        print("Trying to update using primary key value in WHERE")
        results, data = rdb_table.update_by_template(template=template_w_key, new_values=new_values)
        print("Update returned {}\n".format(results), pd.DataFrame(data))
    except TypeError as te:
        print("Could not update: {}".format(str(te)))


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
    results, data = rdb_table.delete_by_template(template=template)
    print("Delete returned {}\n".format(results), pd.DataFrame(data))


t_init()
t_template_to_where_clause()
t_find_by_template()
t_delete_by_template()
t_insert()
t_update_by_template()

