# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib
from credit.vintages import CreditVintage
from credit.forecast import vintage_sett_manual
from common.presentation import tabulate_print


def one_vintage_example():
    """
    A simple example of the construction of a vintage using user
    input data

    """
    roll = [[0.97, 0.03, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
            [0.40, 0.05, 0.55, 0.00, 0.00, 0.00, 0.00, 0.00],
            [0.16, 0.02, 0.02, 0.80, 0.00, 0.00, 0.00, 0.00],
            [0.03, 0.00, 0.00, 0.03, 0.94, 0.00, 0.00, 0.00],
            [0.00, 0.00, 0.00, 0.01, 0.01, 0.98, 0.00, 0.00],
            [0.01, 0.00, 0.00, 0.00, 0.03, 0.02, 0.94, 0.00],
            [0.05, 0.00, 0.00, 0.00, 0.00, 0.00, 0.05, 0.90],
            [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 1.00]]

    sett = vintage_sett_manual(name = 'credioficial',
                               nper = 18,
                               credit_type = 'consumer',
                               sdate = '31-01-2016',
                               forecast = 24,
                               repricing = 0,
                               rate_type = 'FIX',
                               rate_level = 0.2,
                               notional = 10000.0,
                               scores = [0, 30, 60, 90, 120, 150, 180, 210],
                               pay = [0.99, 0.75, 0.55, 0.23, 0.15, 0.05, 0.01,
                                      0.0],
                               prepay = [1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0,
                                         0.0],
                               w_off = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5,
                                        0.5],
                               rolling = {1: roll}
                               )

    vintage = CreditVintage(settings = sett)

    charting = True
    print("##################################################")
    print("         ", vintage.name()), " - Cosecha"
    print("##################################################", '\n')

    tabulate_print(vintage.get_balance(per_score = False))

    print('\n')
    print("##################################################")
    print("             Calidad de Cartera", )
    print("##################################################", '\n')

    quality = vintage.get_quality()
    tabulate_print(quality)

    # charting
    if charting:
        matplotlib.style.use('ggplot')
        quality[['nonperforming', 'nonproductive']].plot(
                title = 'CALIDAD DE CARTERA', linewidth = 5.0)
        plt.show()


if __name__ == '__main__':
    one_vintage_example()
