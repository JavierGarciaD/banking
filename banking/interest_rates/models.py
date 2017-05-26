'''
Created on 11/10/2016

:author: 
:description: Interest rates models
'''


def fixed(nper, level):
    """
    @summary: Simplified version of an interest rate model. 
    @param: nper: number of periods
    @param: level: float
    @return: fixed rate vector for a given number of periods
    """
    return [level] * nper
