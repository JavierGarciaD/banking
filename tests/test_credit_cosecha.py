# -*- coding: utf-8 -*-
# test_credit_cosecha
'''
:summary:
:since: 10/06/2017
:author: spectre
'''
from Cython.Compiler.Errors import message
import pytest

from credit.cosecha2 import rolling_structure
from credit.cosecha2 import value_for_key
import numpy as np
import pandas as pd


@pytest.fixture()
def matrix1():
    return {1:np.matrix([[0.9, 0.1, 0.0],
                         [0.0, 0.5, 0.5],
                         [0.0, 0.0, 1.0]])}


@pytest.fixture()
def ans1_6():
    ''' answer for matrix 1 at 6 months'''
    return np.matrix([[0.59049],
                      [0.13981],
                      [0.2697]])

@pytest.fixture()
def matrix3():
    return {1:np.matrix([[0.6, 0.3, 0.1],
                         [0.2, 0.5, 0.3],
                         [0.1, 0.2, 0.7]])}


@pytest.fixture()
def ans3_36():
    ''' answer for matrix 3 at 36 months'''
    return np.matrix([[0.2647059],
                      [0.3235294],
                      [0.4117647]])


@pytest.fixture()
def matrix2():
    return {1:np.matrix([[0.9, 0.1, 0.0],
                         [0.0, 0.5, 0.5],
                         [0.0, 0.0, 1.0]]),
            2:np.matrix([[0.5, 0.5, 0.0],
                         [0.0, 0.5, 0.5],
                         [0.0, 0.5, 0.5]])}



def test_rolling_structure_m6():
    '''
    vintage structure month 6
    '''
    sdate = pd.to_datetime('31-01-2017')
    nper = 6
    date_index = pd.date_range(sdate, periods = nper, freq = 'M')
    a = rolling_structure(matrix1(), nper, sdate)
    np.testing.assert_allclose(a[date_index[nper - 1]], ans1_6())



def test_rolling_structure_m36():
    '''
    vintage structure month 36
    '''
    sdate = pd.to_datetime('31-01-2017')
    nper = 36
    date_index = pd.date_range(sdate, periods = nper, freq = 'M')
    a = rolling_structure(matrix3(), nper, sdate)
    np.testing.assert_allclose(a[date_index[nper - 1]], ans3_36())



def test_value_for_key_is():
    '''
    :summary: the key is in the dictionary
    '''
    a = value_for_key(matrix2(), 2)
    b = np.matrix([[0.5, 0.5, 0.0],
                   [0.0, 0.5, 0.5],
                   [0.0, 0.5, 0.5]])
    np.testing.assert_allclose(a, b)



def test_value_for_key_is_not():
    '''
    :summary: the key is not in the dictionary
    '''
    a = value_for_key(matrix2(), 12)
    b = np.matrix([[0.9, 0.1, 0.0],
                   [0.0, 0.5, 0.5],
                   [0.0, 0.0, 1.0]])
    np.testing.assert_allclose(a, b)



def test_value_for_key_error():
    '''
    :summary: the key is greater than 12
    '''
    with pytest.raises(KeyError, message = 'the year only have 12 months'):
        value_for_key(matrix2(), 24)




if __name__ == '__main__':
    pytest.main(['-s', '-v', 'test_credit_cosecha.py'])
