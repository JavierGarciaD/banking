# -*- coding: utf-8 -*-
# test_credit_cosecha
"""

:since: Jun 2017
:author: Javier Garcia
"""
import pytest
import numpy as np
import pandas as pd
import datetime as dt
from interest_rates.conversion import compound_effective_yr
from interest_rates.conversion import ea_a_nmv

sdate = pd.to_datetime("01-31-2017")

@pytest.fixture()
def vector_fixed10():
    dates = pd.date_range(start = sdate, periods = 10, freq = 'M')
    return pd.Series([0.02] * 10, index = dates)


@pytest.fixture()
def vector_fixed12():
    dates = pd.date_range(start = sdate, periods = 12, freq = 'M')
    return pd.Series([0.05] * 12, index = dates)


@pytest.fixture()
def vector_variable12():
    dates = pd.date_range(start = sdate, periods = 12, freq = 'M')
    data = np.round([(each_step / 100) + 0.1 for each_step in range(12)], 6)
    return pd.Series(data = data, index = dates)


def test_componer_diff_size(vector_fixed10, vector_variable12):
    with pytest.raises(ValueError):
        compound_effective_yr(fixed_spreads = vector_fixed10,
                              repriced_spread = vector_variable12,
                              repricing = 1)


if __name__ == '__main__':
    pytest.main(['-s', '-v'])

