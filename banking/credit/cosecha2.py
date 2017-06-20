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

from banking.interest_rates.conversion import compound_effective_yr
from banking.interest_rates.conversion import ea_a_nmv
from banking.credit.prepago import psa


or('Rate type unknown!', tipo_tasa)


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