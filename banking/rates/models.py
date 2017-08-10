"""
:author: Javier Garcia
:description: Some interest rates models to choose from
"""
import pandas as pd


class InterestRateModel:
    @staticmethod
    def fixed(nper, sdate, level):
        """

        """
        dates_index = pd.date_range(sdate, periods = nper, freq = 'M')
        return pd.Series([level] * nper, index = dates_index)

    @staticmethod
    def zero(nper, sdate):
        dates_index = pd.date_range(sdate, periods = nper, freq = 'M')
        return pd.Series([0.0] * nper, index = dates_index)

    @staticmethod
    def vasisek():
        # TODO: Vasisek short term rate model
        return NotImplementedError

    @staticmethod
    def random_around_media():
        # TODO: random model
        return NotImplementedError

    @staticmethod
    def linear_g(step, start_level, end):
        # TODO: linear growth
        return NotImplementedError
