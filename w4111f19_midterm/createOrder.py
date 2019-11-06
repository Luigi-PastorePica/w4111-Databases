import json
import pymysql
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

midterm_conn = pymysql.connect(
    host="localhost",
    user="dbuser",
    password="dbuserdbuser",
    cursorclass=pymysql.cursors.DictCursor)

import logging


def run_q(sql, args=None, fetch=True, cur=None, conn=midterm_conn, commit=True):
    '''
    Helper function to run an SQL statement.

    This is a modification that better supports HW1. An RDBDataTable MUST have a connection specified by
    the connection information. This means that this implementation of run_q MUST NOT try to obtain
    a defailt connection.

    :param sql: SQL template with placeholders for parameters. Canno be NULL.
    :param args: Values to pass with statement. May be null.
    :param fetch: Execute a fetch and return data if TRUE.
    :param conn: The database connection to use. This cannot be NULL, unless a cursor is passed.
        DO NOT PASS CURSORS for HW1.
    :param cur: The cursor to use. This is wizard stuff. Do not worry about it for now.
        DO NOT PASS CURSORS for HW1.
    :param commit: This is wizard stuff. Do not worry about it.

    :return: A pair of the form (execute response, fetched data). There will only be fetched data if
        the fetch parameter is True. 'execute response' is the return from the connection.execute, which
        is typically the number of rows effected.
    '''

    cursor_created = False
    connection_created = False

    try:

        if conn is None:
            raise ValueError("In this implementation, conn cannot be None.")

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




def create_order(order_info, cnx):
    """
    Creates (Inserts) the data associated with an order. The order information goes into orders table and each
    and line item/order detail item goes into the ordersdetails table.
    :param order_info: A dictionary. There are top-level elements for the order. There is an orderdetails element
        that is a list of dictionary for the orderdetails elements.
    :param cnx: The database connection to use.
    :return: A tuple of the form (order_insert_count, orderdetals_insert_count), where the values are the number
        of rows inserted into each table.
    """

    #debugging
    order_keys = order_info.keys()
    order_values = []
    for key in order_keys:
        if key != 'orderdetails':
            order_values.append(order_info[key])

    order_detail = []
    for detail in order_info['orderdetails']:
        order_detail.append(detail)


    print(order_keys, order_values)
    print(order_detail)


    max_number_sql = "SELECT MAX(orderNumber) as max_number FROM classicmodels.orders_copy"
    res, data = run_q(max_number_sql, conn=cnx)
    order_number_max = int(data[0]['max_number'])  # This is a temporary hack
    try:
        "Assigns the largest of the two values"
        order_number_given = order_info['orderNumber']

        if order_number_given <= order_number_max:
            order_info['orderNumber'] = order_number_max
    except KeyError as ke:
        order_info['orderNumber'] = order_number_max



    sql_order = "INSERT INTO classicmodels.orders_copy (orderNumber, orderDate, requiredDate, shippedDate, status, comments, customerNumber) values({}, {}, {}, {}, {}, {}, {})".format(order_info['orderNumber'], order_info['orderDate'], order_info['requiredDate'], order_info['shippedDate'], order_info['status'], order_info['comments'], order_info['customerNumber'])

    order_insert_count, data = run_q(sql_order, conn=cnx)
    #orderdetails_insert_count, data = run_q(sql_order_details, conn=cnx)

    #return (order_insert_count, orderdetails_insert_count)
    pass


order = {
           # "orderNumber": 10123,
            "orderDate": "2003-05-20",
            "requiredDate": "2003-05-29",
            "shippedDate": "2003-05-22",
            "status": "Shipped",
            "comments": None,
            "customerNumber": 103,
            "orderdetails": [
                {
                    "orderNumber": 10123,
                    "productCode": "S18_1589",
                    "quantityOrdered": 26,
                    "priceEach": "120.71",
                    "orderLineNumber": 2
                },
                {
                    "orderNumber": 10123,
                    "productCode": "S18_2870",
                    "quantityOrdered": 46,
                    "priceEach": "114.84",
                    "orderLineNumber": 3
                },
                {
                    "orderNumber": 10123,
                    "productCode": "S18_3685",
                    "quantityOrdered": 34,
                    "priceEach": "117.26",
                    "orderLineNumber": 4
                },
                {
                    "orderNumber": 10123,
                    "productCode": "S24_1628",
                    "quantityOrdered": 50,
                    "priceEach": "43.27",
                    "orderLineNumber": 1
                }
            ]
        }

create_order(order, cnx=midterm_conn)