import pymysql

import logging
logger = logging.getLogger()

'''
The default DB connection information. You MUST use this connection information for your assignments
unless we specify otherwise. This means that you will have to:
1. Create the schema lahman2019raw. 
2. 
We will show how to do this.

You MUST create a user dbuser with the password dbuserdbuser.
'''


def _get_default_connection():
    result = pymysql.connect(host='localhost',
                             user='dbuser',
                             password='dbuserdbuser',
                             db='lahman2019raw',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    return result


def run_q(sql, args=None, fetch=True, cur=None, conn=None, commit=True):
    """
    Helper function to run an SQL statement.

    :param sql: SQL template with placeholders for parameters.
    :param args: Values to pass with statement.
    :param fetch: Execute a fetch and return data.
    :param conn: The database connection to use. The function will use the default if None.
    :param cur: The cursor to use. This is wizard stuff. Do not worry about it for now.
    :param commit: This is wizard stuff. Do not worry about it.

    :return: A tuple of the form (execute response, fetched data)
    """

    cursor_created = False
    connection_created = False

    try:

        if conn is None:
            connection_created = True
            conn = _get_default_connection()

        if cur is None:
            cursor_created = True
            cur = conn.cursor()

        if args is not None:
            log_message = cur.mogrify(sql, args)
        else:
            log_message = sql

        logger.debug("Executing SQL = " + log_message)

        res = cur.execute(sql, args)

        if fetch:
            data = cur.fetchall()
        else:
            data = None

        # Do not ask.
        if commit == True:
            conn.commit()

    except Exception as e:
        raise(e)

    return (res, data)


def create_select(table_name, template, fields, order_by=None, limit=None, offset=None):
    """
    Produce a select statement: sql string and args.

    :param table_name: Table name: May be fully qualified dbname.tablename or just tablename.
    :param fields: Columns to select (an array of column name)
    :param template: One of Don Ferguson's weird JSON/python dictionary templates.
    :param order_by: Ignore for now.
    :param limit: Ignore for now.
    :param offset: Ignore for now.
    :return: A tuple of the form (sql string, args), where the sql string is a template.
    """

    if fields is None:
        field_list = " * "
    else:
        field_list = " " + ",".join(fields) + " "

    w_clause, args = template_to_where_clause(template)

    sql = "select " + field_list + " from " +  table_name + " " + w_clause

    return (sql, args)


def template_to_where_clause(template):
    """

    :param template: One of those weird templates
    :return: WHERE clause corresponding to the template.
    """

    if template is None or template == {}:
        result = (None, None)
    else:
        args = []
        terms = []

        for k,v in template.items():
            terms.append(" " + k + "=%s ")
            args.append(v)

        w_clause = "AND".join(terms)
        w_clause = " WHERE " + w_clause

        result = (w_clause, args)

    return result


def create_insert(table_name, row):
    """

    :param table_name: A table name, which may be fully qualified.
    :param row: A Python dictionary of the form: { ..., "column_name" : value, ...}
    :return: SQL template string, args for insertion into the template
    """

    result = "Insert into " + table_name + " "
    cols = []
    vals = []

    # This is paranoia. I know that calling keys() and values() should return in matching order,
    # but in the long term only the paranoid survive.
    for k,v in row.items():
        cols.append(k)
        vals.append(v)

    col_clause = "(" + ",".join(cols) + ") "

    no_cols = len(cols)
    terms = ["%s"]*no_cols
    terms = ",".join(terms)
    value_clause = " values (" + terms + ")"

    result += col_clause + value_clause

    return (result, vals)


def create_update(table_name, new_values, template):
    """

    :param new_values: A dictionary containing cols and the new values.
    :param template: A template to form the where clause.
    :return: An update statement template and args.
    """
    set_terms = []
    args = []

    for k,v in new_values.items():
        set_terms.append(k + "=%s")
        args.append(v)

    s_clause = ",".join(set_terms)
    w_clause, w_args = template_to_where_clause(template)

    # There are %s in the SET clause and the WHERE clause. We need to form
    # the combined args list.
    args.extend(w_args)

    sql = "update " + table_name + " set " + s_clause + " "+ w_clause

    return sql, args


