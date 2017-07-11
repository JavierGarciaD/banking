# -*- coding: utf-8 -*-
# conversion
"""
:summary: some fuction for interest rate transforms
:author: Javier Garcia
:since: 10-06-2017
"""
import numpy as np


def ea_a_nmv(vector_a):
    """
    :param: pandas series of effective annual rates
    :return: pandas series of nominal monthly rates
    """
    return np.round(vector_a.apply(lambda r: (1 + r) ** (1 / 12) - 1), 6)


def compound_effective_yr(fixed_spreads, repriced_spread, repricing = 1):
    """

    :param fixed_spreads: pandas series of effective annual spread
    :param repriced_spread: pandas series of effective anual variable rates
    :param repricing: frequency of repricing 1:monthly, 2:bimonthly,
    3: Quarterly, etc.
    :return: pandas series of effective annual rates with repricing
    """

    if not fixed_spreads.index.equals(repriced_spread.index):
        raise ValueError("Vectores de tasas con diferente tamaño !")

    repriced = pd.Series(data = 0.0, index = fixed_spreads.index)
    for row in repriced.index:
        residual = fixed_spreads.index.get_loc(row) % repricing
        if residual == 0:
            applicable_r = repriced_spread[row]
        else:
            applicable_r = repriced_spread[row - residual]
        repriced[row] = (1 + fixed_spreads[row]) * (1 + applicable_r) - 1
    return repriced



if __name__ == '__main__':
    import pandas as pd

    ind0 = pd.date_range(start = pd.to_datetime('31-12-2017'),
                         periods = 12, freq = 'M')
    ind1 = pd.date_range(start = pd.to_datetime('31-01-2017'),
                         periods = 10, freq = 'M')

    x = pd.Series([0.3] * 10, index = ind1)

    y = pd.Series([0.2] * 12, index = ind0)

    z = pd.Series([0.1, 0.09, 0.08, 0.07, 0.06, 0.05, 0.04, 0.03, 0.02, 0.01,
                   0.0, 0.0], index = ind0)

    # ans0 = ea_a_nmv(x)
    # print(ans0)
    # print(type(ans0))

    ans = compound_effective_yr(fixed_spreads = x, repriced_spread = y,
                                repricing = 1)
    print(ans)
