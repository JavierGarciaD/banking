'''
Created on 11/10/2016

@author: javgar119
'''

import pandas as pd
import os


#===============================================================================
# 1. Import all the settings for products, clients, budgets, etc
#===============================================================================
pathname = 'file://s-80cw4/compartidos/GerenciaFinanciera/07. Rentabilidad de Productos/Modelos de rentabilidad/Info_proyection.xlsx'


xls_file = pd.ExcelFile(pathname)






if __name__ == '__main__':
    print(pathname)
    print(xls_file.type())