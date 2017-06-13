# -*- coding: utf-8 -*-
# conversion
"""
:summary: some fuction for interest rate transforms
:author: Javier Garcia
:since: 10-06-2017
"""


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
    if vector_a.size == vector_b.size:
        return (1 + vector_a) * (1 + vector_b) - 1
    else:
        raise ValueError("Vectores de tasas con diferente tamaño !")


if __name__ == '__main__':
    import timeit
    import pandas as pd
    x = pd.Series([0.12431341, ] * 10, index=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    y = pd.Series([0.1213124124] * 12, index=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    z = pd.Series([0.1213124124] * 12, index=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])

    a = timeit.Timer('componer_efectivas(y,z)', setup="from __main__ import  \
        componer_efectivas, y, z").timeit(number=1000)

    print(a)


