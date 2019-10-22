import HW_Assignments.HW2F19_Template.src.data_service.data_table_adaptor as dtadaptor
import json
import pandas as pd

_test_connection = {
    'host': 'localhost',
    'user': 'root',
    'password': 'dbuserdbuser',
    'db': 'lahman2019clean',
    'port': 3306
}


def t_get_rdb_table():

    global _test_connection

    rdb_table = dtadaptor.get_rdb_table(table_name='people', db_name='lahman2019clean', connect_info=_test_connection)
    print(rdb_table)


def t_get_databases():

    db_list = dtadaptor.get_databases()
    # print("The list of databases is:\n\n {}".format(json.dumps(dbList, indent=2))) # Print as pretty json
    print("The list of databases is:\n\n{}\n".format(pd.DataFrame(db_list))) # Print as DataFrame (i.e. spreadsheet)

def t_get_tables():

    tbl_list = dtadaptor.get_tables()
    # print("The list of databases is:\n\n {}".format(json.dumps(tblList, indent=2))) # Print as pretty json
    print("The list of tables is:\n\n{}\n".format(pd.DataFrame(tbl_list)))  # Print as DataFrame (i.e. spreadsheet)

t_get_rdb_table()
t_get_databases()
t_get_tables()