'''
Created on 11/10/2016

@author: javgar119
'''
import pandas as pd


pathname = "C:/Users/javgar119/GIT/banking/banking/data/info_proyeccion.xlsx"
xls_file = pd.ExcelFile(pathname)
#===============================================================================
# import client's settings 
#===============================================================================
client_nodes = xls_file.parse('nodes')
client_distribution = xls_file.parse('clientes')

#===============================================================================
# import product's settings
#===============================================================================
product_settings = xls_file.parse('productos')
product_budget = xls_file.parse('presupuesto')
product_contractual_cf_k = xls_file.parse('flujo_contractual')
product_contractual_rates = xls_file.parse('tasa_contractual')







 
    
    
if __name__ == '__main__':
    print(product_budget)
