# -*- coding: utf-8 -*-
# conversion
"""
:summary: some fuction for interest rate transforms
:author: Javier Garcia
:since: 10-06-2017
"""


def ea_a_nmv(vector_a):
    """

    :param vector_a:
    :return:
    """
    return vector_a.apply(lambda r: (1 + r) ** (1 / 12) - 1)


def compound_effective_yr(spreads, variable_rate, repricing = 1):
    """

    :return:
    """

    if not spreads.index.equals(variable_rate.index):
        raise ValueError("Vectores de tasas con diferente tamaño !")

    reprice = pd.Series(data = 0.0, index = spreads.index)

    for row in spreads.index:
        res = spreads.index.get_loc(row) % repricing

        if res == 0:
            applicable_r = variable_rate[row]
        else:
            applicable_r = variable_rate[row - res]

        reprice[row] = (1 + spreads[row]) * (1 + applicable_r) - 1

    print(reprice)


    #return v_with_reprice


if __name__ == '__main__':
    import timeit
    import pandas as pd

    ind0 = pd.date_range(start = pd.to_datetime('31-12-2017'),
                         periods = 12, freq = 'M')
    ind1 = pd.date_range(start = pd.to_datetime('31-01-2017'),
                         periods = 10, freq = 'M')
    x = pd.Series([0.12431341, ] * 10, index = ind1)

    y = pd.Series([0.1213124124] * 12, index = ind0)

    z = pd.Series([0.1, 0.09, 0.08, 0.07, 0.06, 0.05, 0.04, 0.03, 0.02, 0.01,
                   0.0, 0.0], index = ind0)


    ans = compound_effective_yr(spreads = y,
                                variable_rate = z, repricing = 3)

