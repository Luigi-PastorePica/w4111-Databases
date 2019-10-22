import pymysql
import HW_Assignments.HW2F19_Template.src.data_service.dbutils as dbutils
import HW_Assignments.HW2F19_Template.src.data_service.RDBDataTable as RDBDataTable

# The REST application server app.py will be handling multiple requests over a long period of time.
# It is inefficient to create an instance of RDBDataTable for each request.  This is a cache of created
# instances.
_db_tables = {}

# Placing the connection information here is a hack implemented in office hours. I will be using this in the meantime
# for the sake of time. What I would do if I had more time: Something similar to what one of the CAs suggested, which is
# having RDBDataTable have None default values for table_name and db_name. In case such values were Null, connect_info
# would have to be provided. I think in this way it would make sense to have a function return the connect info.
_connect_info = pymysql.connect(
    host='localhost',
    user='root',
    password='dbuserdbuser',
    db='lahman2019clean',
    port=3306,
    cursorclass=pymysql.cursors.DictCursor
)



def get_rdb_table(table_name, db_name, key_columns=None, connect_info=None):
    """

    :param table_name: Name of the database table.
    :param db_name: Schema/database name.
    :param key_columns: This is a trap. Just use None.
    :param connect_info: You can specify if you have some special connection, but it is
        OK to just use the default connection.
    :return:
    """
    global _db_tables

    # We use the fully qualified table name as the key into the cache, e.g. lahman2019clean.people.
    key = db_name + "." + table_name

    # Have we already created and cache the data table?
    result = _db_tables.get(key, None)

    # We have not yet accessed this table.
    if result is None:

        # Make an RDBDataTable for this database table.
        result = RDBDataTable.RDBDataTable(table_name, db_name, key_columns, connect_info)

        # Add to the cache.
        _db_tables[key] = result

    return result


#########################################
#
#
# YOU HAVE TO IMPLEMENT THE FUNCTIONS BELOW.
#
#
# -- TO IMPLEMENT --
#########################################

def get_databases():
    """

    :return: A list of databases/schema at this endpoint.
    """

    global _connect_info

    sql = "SHOW DATABASES"
    res, data = dbutils.run_q(sql, conn=_connect_info) # This is a temporary hack
    return data


def get_tables():

    global _connect_info

    sql = "SHOW TABLES"
    res, data = dbutils.run_q(sql, conn=_connect_info) # This is a temporary hack
    return data





