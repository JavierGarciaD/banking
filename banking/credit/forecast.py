# -*- coding: utf-8 -*-
from common.db_manager import forecast_db
from sqlalchemy import select
from sqlalchemy import and_


def get_contract_info(product_name):
    """
    Get contract info from forecast database
    :return: dict with nper, rate_type, repricing for a given product
    """
    db = forecast_db()
    conn = db[0]
    meta = db[1]
    table = meta.tables['contract_info']

    # Construct select sql statement
    sql = select([table]).where(
            table.c.product_name == product_name)

    # execute and fetch result
    ans = conn.execute(sql)
    row = ans.fetchone()

    # Close the connection
    ans.close()
    conn.close()

    # Construct dictionary
    return dict(nper = row[1],
                rate_type = row[2],
                repricing = row[3],
                rate_spread = row[4])


def get_rolling(product_name, m):
    """
    Get the rolling matrix for a specific product and month
    :param product_name:
    :param m: month
    :return: list of list rolling matrix
    """
    db = forecast_db()
    conn = db[0]
    meta = db[1]
    table = meta.tables['rolling']

    # Construct select sql statement
    sql = select([table.c.rolling0,
                  table.c.rolling30,
                  table.c.rolling60,
                  table.c.rolling90,
                  table.c.rolling120,
                  table.c.rolling150,
                  table.c.rolling180]).where(
            and_(table.c.product_name == product_name,
                 table.c.month == m))

    print(sql)
    # Execute and fetch result
    ans = conn.execute(sql).fetchall()[0]

    # Close the connection
    conn.close()

    # Parse and create list of list
    ret = []
    for row in ans:
        parsed_list = row.split(",")
        dbl_list = [float(x) for x in parsed_list]
        ret.append(dbl_list)

    return ret


def rolling_dict(product_name):
    pass


if __name__ == '__main__':
    from pprint import pprint
    x = get_rolling('tarjeta de credito', 1)
    pprint(x)
