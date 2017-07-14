# -*- coding: utf-8 -*-
"""
:author: MacroTrader
:email:  javier.macro.trader@gmail.com
:summary: different pre-payment models to choose from

"""
import numpy as np
import pandas as pd


class PrepaymentModel:
    """
    Group of prepayment functions
    """
    @staticmethod
    def zero(nper):
        """
        @summary: zero prepayment model, there is not prepayment
        """
        return [0.] * nper

    @staticmethod
    def linear(nper, ceil):
        """
        @summary: Simple linear prepayment, clients always prepay the same % value
        @param nper: int number of periods
        @param ceil: float,
        @return: constant list of monthly prepayment rates
        """
        return np.round([ceil] * nper, 6)

    @staticmethod
    def psa(nper, ceil, stable_period):
        """
        Variation of the Public Securities Association (PSA) prepayment model
        for Mortgage Backed Securities.
        https://en.wikipedia.org/wiki/PSA_prepayment_model

        :param nper: int
        :param ceil: float
        :param stable_period: int
        :return: prepayment numpy array
        """
        step = ceil / stable_period
        return np.round([step * each_per if step * each_per <= ceil else
                         ceil for each_per in range(0, nper + 1)], 6)
