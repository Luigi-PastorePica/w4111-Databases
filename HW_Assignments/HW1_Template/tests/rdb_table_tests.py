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

t_init()
t_template_to_where_clause()
t_find_by_template()