# -*- coding: utf-8 -*-
from common.db_manager import forecast_db
from sqlalchemy import select
from sqlalchemy import and_
from sqlalchemy import asc


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


def get_scores():
    """

    :return: list with available scores
    """
    db = forecast_db()
    conn = db[0]
    meta = db[1]
    table = meta.tables['scores']

    sql = select([table.c.score]).order_by(asc('score'))
    ans = conn.execute(sql)

    ret = []
    for row in ans:
        ret.append(int(row[0]))

    conn.close()
    return ret


def get_rolling(product_name):
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

    scores = get_scores()
    ans_dict = dict()
    for each_month in range(12):
        ret = []
        for each_score in scores:
            # roll for product x score x month
            sql = select([table.c.roll]).where(
                    and_(table.c.product_name == product_name,
                         table.c.month == each_month + 1,
                         table.c.score == each_score))

            # Execute and fetch result
            ans = conn.execute(sql).fetchall()[0]

            # Parse and create list of list
            for row in ans:
                parsed_list = row.split(",")
                dbl_list = [float(x) for x in parsed_list]
                ret.append(dbl_list)

        ans_dict[each_month + 1] = ret

    conn.close()

    return ans_dict


if __name__ == '__main__':


    x = get_rolling('tarjeta de credito')
    print(x)

