# -*- coding: utf-8 -*-
'''
:author: MacroTrader
:email:  javier.macro.trader@gmail.com
Created on 30/10/2016


Description: different prepayment models

'''


def zero(nper):
    """
    zero prepayment model, there is not prepayment
    """
    return [0.] * nper


def linear(nper, level=0.03):
    """
    Simple linear prepayment, clients always prepay the same % value
    :param nper: int number of periods
    :param level: float, 
    :return: constant list of monthly prepayment rates
    """
    return [level] * nper


def psa(nper, ceil=0.03, stable_per=24):
    """
    Variation of the Public Securities Association (PSA) prepayment model for Mortgage Backed Securities.
    https://en.wikipedia.org/wiki/PSA_prepayment_model
    :param nper: int
    :param ceil: float
    :param stable_per: int
    :return: prepayment rate list
    """

    ans = [0.] * nper
    step = ceil / stable_per
    for each_per in range(0, nper):
        if (step * each_per) <= ceil:
            ans[each_per] = step * each_per
        else:
            ans[each_per] = ans[each_per - 1]
    return ans
