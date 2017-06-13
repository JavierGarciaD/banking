# -*- coding: utf-8 -*-
# test_credit_cosecha
"""
:summary:
:since: Jun 2017
:author: Javier Garcia
"""
import pytest
import numpy as np
import pandas as pd
from interest_rates.conversion import componer_efectivas
from interest_rates.conversion import efectiva_a_nmv


@pytest.fixture()
def vector_a():
    return pd.Series([0.1, 0.2])


@pytest.fixture()
def vector_b():
    return pd.Series([0.3, 0.4, 0.5])


@pytest.fixture()
def vector_c():
    return pd.Series([0.1, 0.2, 0.3])


def test_componer_result():
    ans = [0.43, 0.68, 0.95]
    np.testing.assert_allclose(componer_efectivas(vector_b(), vector_c()), ans)


def test_componer_diff_size():
    with pytest.raises(ValueError):
        componer_efectivas(vector_a(), vector_b())


if __name__ == '__main__':
    pytest.main(['-s', '-v'])
