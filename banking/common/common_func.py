"""
Created on 11/10/2016

@author: javgar119
"""
import pandas as pd



pathname = "C:/Users/javgar119/GIT/banking/banking/data/info_proyeccion.xlsx"
xls_file = pd.ExcelFile(pathname)
product_12m_budget = xls_file.parse('presupuesto')

def budget_proyection(one_year_budget, lenght_proyection, inflation, productivity):
    """
    todo:
    """
    
    




if __name__ == '__main__':
    ans = budget_proyection(product_12m_budget, 120, 0.06, 0.01)
    print(ans)