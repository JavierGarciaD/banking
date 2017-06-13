"""
Created on 11/10/2016

:author:
:description: Interest rates models
"""
import pandas as pd


def fixed(nper, fecha_inicial, level):
    """

    """
    dates_index = pd.date_range(fecha_inicial, periods = nper, freq = 'M')
    
    return pd.Series([level] * nper, index = dates_index)

