"""
Created on 9/06/2017

@author: spectre
"""
from os.path import expanduser
import pandas as pd
from tabulate import tabulate
# https://pypi.python.org/pypi/tabulate


def tabulate_print(data):
    """
    Print nicely the vintage results
    :param: vintage: credit vintage object
    :return: console output
    """
    print(tabulate(data,
                   headers = 'keys',
                   numalign = 'right',
                   tablefmt = 'simple',
                   floatfmt = ",.2f"))


def save_to_xls(name):
    writer = pd.ExcelWriter(expanduser('~') + '/PycharmProjects/banking/'
                                              'data/' + name + '.xls')
    name.transpose().to_excel(writer)
    writer.save()
    print("SAVE TO XLS, DONE!")
