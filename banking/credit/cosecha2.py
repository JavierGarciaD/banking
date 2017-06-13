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


def output_structure(sdate, nper, scores):
    """
    :param scores:
    :summary: construct the pandas dataframe output for a vintage
    structure

    :param nper: forecasting periods
    :param sdate: starting date

    :type sdate: datetime
    :type nper: int

    :return: dataframe with score structure
    :rtype: pandas dataframe
    """

    col_names = ['saldo_inicial',
                 'desembolso',
                 'amortizacion',
                 'prepago',
                 'castigo',
                 'saldo_final']

    cols = []
    for each_col in col_names:
        for each_score in scores:
            cols.append(each_col + str(each_score))

    dates_index = pd.date_range(sdate, periods=nper, freq='M')
    ans = pd.DataFrame(0.0,
                       index=dates_index,
                       columns=cols)
    return ans


def rolling_structure(d_matrix, nper, sdate):
    """
    :summary: construct the score structure of a credit vintage, given
    a rolling matrix

    :param d_matrix: dict with 1 or 12 rolling matrix
    :param nper: forecasting periods
    :param sdate: starting date

    :type d_matrix: dict of numpy matrix
    :type sdate: datetime
    :type nper: int

    :return: vintage structure over time
    :rtype: numpy matrix
    """

    dates_index = pd.date_range(sdate, periods=nper, freq='M')
    ans_dict = dict.fromkeys(dates_index)

    # setup of first month
    ans0 = np.asmatrix(np.zeros((d_matrix[1].shape[0], 1)))
    ans0[(0, 0)] = 1.0

    for key in dates_index:
        m = value_for_key(d_matrix, key.month)
        if key == dates_index[0]:
            ans_dict[key] = ans0
        else:
            ans_dict[key] = np.transpose(m) * ans_dict[key - 1]

    return ans_dict


def value_for_key(dict_matrix, key):
    """
    :summary: find the right matrix (val) given a month (key)
    check for months beyond 12 (dec)

    :param dict_matrix: dict with 1 or 12 rolling matrix
    :param key: month to find 1 to 12

    :type dict_matrix: dict of numpy matrix
    :return: rolling matrix for a given month
    :rtype: numpy matrix
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
    :summary: compute monthly nominal rate from a series of annual rates.
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
        return np.round(efectiva_a_nmv(spread_orig), 6)
    elif tipo_tasa == "DTF" or tipo_tasa == "IPC":
        vector_full = componer_efectivas(index_vector, spreads_vector)
        return np.round(efectiva_a_nmv(vector_full), 6)
    elif tipo_tasa == "IBR":
        pass
    else:
        raise ValueError('Rate type unknown!', tipo_tasa)


def efectiva_a_nmv(vector_a):
    """

    :param vector_a:
    :return:
    """
    return vector_a.apply(lambda tasa: (1 + tasa) ** (1 / 12) - 1)


def componer_efectivas(vector_a, vector_b):
    """
    :param vector_a:
    :param vector_b:
    :return:
    """
    return (1 + vector_a) * (1 + vector_b) - 1


if __name__ == '__main__':
    import banking.interest_rates.models as models
    import timeit

    m = {1: np.matrix([[0.9, 0.1, 0.0],
                       [0.0, 0.5, 0.5],
                       [0.0, 0.0, 1.0]])}
    scores = [0, 30, 60, 90]
    d = pd.to_datetime('31-01-2017')

    spread_orig = models.fixed(12, d, 0.22)
    vector_tasas_indice = pd.Series(
            [0.07, 0.08, 0.09, 0.05, 0.04, 0.07, 0.06, 0.05, 0.05, 0.09, 0.08, 0.03],
            index=spread_orig.index)

    output = tasas_full_nmv('DTF', spread_orig, vector_tasas_indice)

    a = timeit.Timer("tasas_full_nmv('DTF', spread_orig, vector_tasas_indice)",
                     setup="from __main__ import tasas_full_nmv, spread_orig, \
                            vector_tasas_indice").timeit(number=1000)
    print(a)
