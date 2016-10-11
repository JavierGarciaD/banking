'''
Created on 11/10/2016

:author: 
:description: some simplification of interest rates models
'''


class InterestRateModel:
    def __init__(self):
        pass

    @staticmethod
    def fixed(nper, level):
        """
        Simple list of monthly rates
        :param nper: nper
        :param level: float
        :return: list of rates x nper
        """
        return [level] * nper