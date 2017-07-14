# -*- coding: utf-8 -*-
from common.db_manager import DB
from sqlalchemy import select
from sqlalchemy import and_
from sqlalchemy import asc


def get_contract_info(product_name):
    """
    Get contract info from forecast database
    :return: dict with nper, rate_type, repricing for a given product
    """
    db = DB('forecast')
    table = db.table('contract_info')

    # Construct select sql statement
    sql = select([table.c.nper,
                  table.c.rate_type,
                  table.c.repricing,
                  table.c.rate_spread]).where(
            table.c.product_name == product_name)

    # execute and fetch result
    ans = db.query(sql).fetchone()

    # Construct dictionary
    return dict(nper = int(ans[0]),
                rate_type = str(ans[1]),
                repricing = int(ans[2]),
                rate_spread = float(ans[3]))


def get_scores():
    """

    :return: list with available scores
    """
    db = DB('forecast')
    table = db.table('scores')

    sql = select([table.c.score]).order_by(asc('score'))
    ans = db.query(sql)

    ret = []
    for row in ans:
        ret.append(int(row[0]))

    return ret


def get_rolling(product_name):
    """
    Get the rolling matrixes for a specific product
    :param product_name:
    :return: dict with rolling matrix for each month
    """
    db = DB('forecast')
    table = db.table('rolling')
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
            ans = db.query(sql).fetchone()

            # Parse and create list of list
            for row in ans:
                parsed_list = row.split(",")
                float_list = [float(x) for x in parsed_list]
                ret.append(float_list)

        ans_dict[each_month + 1] = ret

    return ans_dict


def get_prepay_per_score():
    # TODO: get_prepay_per_score
    return NotImplementedError


def get_writeoff_per_score():
    # TODO: get_writeoff_per_score
    return NotImplementedError


def get_pay_per_score():
    # TODO: get_pay_per_score
    return NotImplementedError


if __name__ == '__main__':

    scr = get_contract_info('tarjeta de credito')
    print(scr)
    score = get_scores()
    print(score)
    x = get_rolling('tarjeta de credito')
    print(x)

