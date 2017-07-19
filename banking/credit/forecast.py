# -*- coding: utf-8 -*-
import pandas as pd
from rates.models import InterestRateModel
from common.db_manager import DB
from sqlalchemy import select
from sqlalchemy import and_
from sqlalchemy import asc


def get_contract_info(product_name):
    """
    Get contract info from forecast database
    :return: dict with nper, rate_type, repricing_ rate_spread. And per score
    provision, payment probability, prepayment probability, writeoff prob.
    """
    db = DB('forecast')
    ########################################
    # Query contract info
    ########################################
    table = db.table('contract_info')
    sql = select([table.c.nper,
                  table.c.rate_type,
                  table.c.repricing,
                  table.c.rate_spread]).where(
            table.c.product_name == product_name)

    # execute and fetch result
    ans = db.query(sql).fetchone()

    ans_dict = dict(nper = int(ans[0]),
                    rate_type = str(ans[1]),
                    repricing = int(ans[2]),
                    rate_spread = float(ans[3]))

    return ans_dict


def get_credit_info(product_name):
    db = DB('forecast')
    table = db.table('credit_info')
    scores = get_scores()
    ans_dict = dict()

    sql = select([table.c.payment,
                  table.c.prepayment,
                  table.c.provision,
                  table.c.writeoff]).where(table.c.product_name ==
                                           product_name).order_by(asc('score'))

    # Execute and fetch result
    ans = db.query(sql)

    pay = []
    pre = []
    prov = []
    wo = []
    for row in ans:
        pay.append(row[0])
        pre.append(row[1])
        prov.append(row[2])
        wo.append(row[3])

    ans_dict['pay_per_score'] = pd.Series(data = pay, index = scores)
    ans_dict['prepay_per_score'] = pd.Series(data = pre, index = scores)
    ans_dict['provision_per_score'] = pd.Series(data = prov, index = scores)
    ans_dict['writeoff_per_score'] = pd.Series(data = wo, index = scores)

    return ans_dict


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
            sql = select([table.c.roll0,
                          table.c.roll30,
                          table.c.roll60,
                          table.c.roll90,
                          table.c.roll120,
                          table.c.roll150,
                          table.c.roll180]).where(
                    and_(table.c.product_name == product_name,
                         table.c.month == each_month + 1,
                         table.c.score == each_score))

            # Execute and fetch result
            ans = list(db.query(sql).fetchone())
            ret.append(ans)

        ans_dict[each_month + 1] = ret
    return ans_dict


def get_budget(product_name, sdate):
    """
    Budget for a product, limited to data available at the database
    :param product_name:
    :param sdate: starting date
    :return: pandas series
    """
    db = DB('forecast')
    table = db.table('budget')

    sql = select([table.c.budget]).where(table.c.product_name ==
                                         product_name).order_by(asc('month'))
    ans = db.query(sql).fetchall()

    ret = []
    for row in ans:
        ret.append(float(row[0]))

    date_index = pd.date_range(start = sdate, periods = len(ret), freq = 'M')

    return pd.Series(data = ret, index = date_index)


def vintage_settings(product_name, sdate,
                     disburment, fore_length,
                     prepay_array, index_array):

    # Gets information from forecast database about the contract_info:
    contract_info = get_contract_info(product_name)
    # Gets information from forecast database about the credit_info:

    credit_info = get_credit_info(product_name)
    # spread over index is fixed
    spreads_array = InterestRateModel.fixed(nper = fore_length,
                                            sdate = sdate,
                                            level = contract_info[
                                                'rate_spread'])

    settings = dict(name = product_name,
                    nper = contract_info['nper'],
                    rate_type = contract_info['rate_type'],
                    repricing = contract_info['repricing'],
                    forecast = int(fore_length),
                    scores = get_scores(),
                    sdate = pd.to_datetime(sdate),
                    notional = float(disburment),
                    index_rates_array = index_array,
                    rate_spreads_array=spreads_array,
                    prepay_array=prepay_array,
                    prepay_per_score=credit_info['prepay_per_score'],
                    rolling_m=get_rolling(product_name),
                    pay_per_score=credit_info['pay_per_score'],
                    writeoff_per_score=credit_info['writeoff_per_score']
                    )

    return settings


# def provision_por_calificacion():
#      return {0: 0.10,
#             30: 0.15,
#             60: 0.25,
#             90: 0.40,
#             120: 0.60,
#             150: 0.80,
#             180: 1.00
#     }


if __name__ == '__main__':
    from pprint import pprint

    # scr = get_contract_info('tarjeta de credito')
    # pprint(scr)
    # score = get_scores()
    # print(score)
    # x = get_rolling('tarjeta de credito')
    # print(x)
    bdg = get_budget('tarjeta de credito', '31-01-2017')
    print(bdg)
    # x = get_credit_info('tarjeta de credito')
    # pprint(x)
