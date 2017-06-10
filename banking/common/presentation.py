'''
Created on 9/06/2017

@author: spectre
'''
from os.path import expanduser
from tabulate import tabulate
# https://pypi.python.org/pypi/tabulate

def print_tabulate(data):
    """
    Print nicely the vintage results
    :param: vintage: credit vintage object
    :return: console output
    """


    print(tabulate(data,
                   headers = 'keys',
                   numalign = 'right',
                   tablefmt = 'fancy_grid',
                   floatfmt = ",.2f"))


def save_to_xls(bol, name):
    if bol == True:
        writer = pd.ExcelWriter(expanduser('~') + '/git/banking/data/' + name + '.xlsx')
        name.transpose().to_excel(writer)
        writer.save()
        print("SAVE TO XLS, DONE!")


