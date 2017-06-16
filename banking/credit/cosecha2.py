# -*- coding: utf-8 -*-
# cosecha
"""
:summary: A collection of classes and functions to forecast credit vintages
:author: Javier Garcia
:since: 10-06-2017
"""
# from common.presentation import print_tabulate
import numpy as np
import pandas as pd

from banking.interest_rates.conversion import componer_efectivas
from banking.interest_rates.conversion import ea_a_nmv
from banking.credit.prepago import psa




def rolling_structure(d_matrix, nper, sdate):
    """
    Construct the score structure of a credit vintage, given
    a rolling matrix

    :param d_matrix: dict of numpy matrix, with 1 or 12 rolling matrix
    :param nper:  int forecasting periods
    :param sdate: datetime starting date

    :return: numpy matrix of vintage structure over time
     """
    # dictionary structure
    ans_dict = dict.fromkeys(pd.date_range(sdate, periods=nper, freq='M'))
    # setup of first month
    ans0 = np.asmatrix(np.zeros((d_matrix[1].shape[0], 1)))
    ans0[(0, 0)] = 1.0

    for key in sorted(ans_dict.keys()):
        m_to_apply = value_for_key(d_matrix, key.month)
        if key == sorted(ans_dict.keys())[0]:
            ans_dict[key] = ans0
        else:
            ans_dict[key] = np.transpose(m_to_apply) * ans_dict[key - 1]
    return ans_dict


def value_for_key(dict_matrix, key):
    """
    :summary: find the right matrix (val) given a month (key)
    check for months beyond 12 (dec)

    :param dict_matrix: dict with 1 or 12 rolling matrix
    :param key: month to find 1 to 12

    :return: numpy matrix rolling matrix for a given month
    """
    # look for the right matrix given a month
    # if there is not a matrix for a given month take the # 1
    if key > 12:
        raise KeyError
    elif key in dict_matrix.keys():
        return dict_matrix[key]
    else:
        return dict_matrix[1]


def tasas_full_nmv(tipo_tasa, spreads_vector, index_vector):
    """
    Compute monthly nominal rate from a series of annual rates.
    Computation formula given the index characteristics.

    :param tipo_tasa: 'FIJA', 'DTF', 'IBR', 'IPC'
    :param spreads_vector: annual rates for the spread
    :param index_vector: annual rate for the index that apply at every period

    :type tipo_tasa: str
    :type spreads_vector: pandas serie
    :type index_vector: pandas serie

    :return: nominal rate that apply at each period
    :rtype: pandas serie
    """
    tipo_tasa = tipo_tasa.upper()

    if tipo_tasa == "FIJA":
        return np.round(ea_a_nmv(spread_orig), 6)
    elif tipo_tasa == "DTF" or tipo_tasa == "IPC":
        vector_full = componer_efectivas(index_vector, spreads_vector)
        return np.round(ea_a_nmv(vector_full), 6)
    elif tipo_tasa == "IBR":
        #########################################
        # TODO implementacion de calculo para IBR
        #########################################
        pass
    else:
        raise ValueError('Rate type unknown!', tipo_tasa)


def cosecha(val, plazo, fecha1, nper, tipo_tasa, spreads_v, indices_v, \
                                                rolling_m,
            prepago_v):

    ans_df = output_structure(fecha1, nper, rolling_m['scores'])
    tasa_v = tasas_full_nmv()
    for row in ans_df.iterrows():
        # desembolso
        if row[0] == fecha1:
            ans_df.loc[row[0], 'desembolso_0'] = val
            ans_df.loc[row[0], 'saldo_final_0'] = val



    return ans_df


if __name__ == '__main__':
    import banking.interest_rates.models as models

    m = {
        1: np.matrix([[0.9, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                      [0.5, 0.1, 0.4, 0.0, 0.0, 0.0, 0.0, 0.0],
                      [0.3, 0.0, 0.1, 0.6, 0.0, 0.0, 0.0, 0.0],
                      [0.2, 0.0, 0.0, 0.2, 0.6, 0.0, 0.0, 0.0],
                      [0.1, 0.0, 0.0, 0.0, 0.1, 0.8, 0.0, 0.0],
                      [0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.9, 0.0],
                      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3, 0.7],
                      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]]),
        'scores': [0, 30, 60, 90, 120, 150, 180, 210]
        }

    sdate = pd.to_datetime('31-01-2017')
    per = 12
    i_orig = models.fixed(per, sdate, 0.22)
    i_indice = pd.Series([0.0]*per, index=i_orig.index)
    i_prepay = psa(nper = 24, sdate = sdate)

    # roll = rolling_structure(m, 12, d)
    # pprint(roll)

    #structure = output_structure(d, 12, calif)
    #print(structure)

    # output = tasas_full_nmv('DTF', spread_orig, vector_tasas_indice)
    # print(output)

    c1 = cosecha(val = 10000.0, plazo = per, nper = 24, fecha1 = sdate,
                 spreads_v = i_orig, tipo_tasa = 'FIJA', indices_v = i_indice,
                 rolling_m = m, prepago_v = i_prepay)

    print(c1)