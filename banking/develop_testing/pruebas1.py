# -*- coding: utf-8 -*-
'''
:author: MacroTrader
:email:  javier.macro.trader@gmail.com
Created on 30/10/2016

Description:

'''


import credit.constructor as constructor
import credit.prepayment as prepayment
import interest_rates.models as i_models


if __name__ == '__main__':
    proyeccion = 60
    producto = 'pyme'
    plazo = 24
    tasas = i_models.InterestRateModel.fixed(plazo, 0.0145)
    prepago = prepayment.psa(nper=plazo,
                             ceil=0.03,
                             stable_per=12)

    modelo_credito = constructor.CreditModel.simple(nper=plazo,
                                                    loss=0.02)
    presupuesto = [20000] * proyeccion

    cont_conditions = dict(balance=0.0,
                           ppmt=[0.0 / plazo] * plazo,
                           fixed_rate=[0.012] * plazo,
                           spread_DTF=None,
                           spread_IBR=None,
                           repricing=None)

    cosecha_contractual = constructor.contractual_vintage(
        cont_conditions, prepago, modelo_credito)

    cosechas = constructor.collection_of_vintages(producto, proyeccion, plazo, tasas, prepago,
                                                  modelo_credito, presupuesto, 'consolidate')

    cosechas_total = cosechas.add(cosecha_contractual, fill_value=0)
    constructor.print_vintage(cosechas_total)
