

import credit.constructor
import credit.constructor_cosechas as constructor
import credit.prepayment
import interest_rates.models
import pandas as pd




def correr_constructor_antiguo():
    proyeccion = 60
    producto = 'pyme'
    plazo = 24
    tasas = interest_rates.models.fixed(plazo, 0.0145)
    prepago = credit.prepayment.psa(nper = plazo, ceil = 0.03, stable_per = 12)

    modelo_credito = credit.constructor.CreditModel.simple(nper = plazo,
                                                           loss = 0.02)
    presupuesto = [20000] * proyeccion

    cont_conditions = dict(constructor_de_balance = 0.0,
                           ppmt = [0.0 / plazo] * plazo,
                           fixed_rate = [0.012] * plazo,
                           spread_DTF = None,
                           spread_IBR = None,
                           repricing = None)

    cosecha_contractual = credit.constructor.contractual_vintage(
        cont_conditions, prepago, modelo_credito)

    cosechas = credit.constructor.collection_of_vintages(producto,
                                                         proyeccion,
                                                         plazo,
                                                         tasas,
                                                         prepago,
                                                         modelo_credito,
                                                         presupuesto,
                                                         'consolidate')

    cosechas_total = cosechas.add(cosecha_contractual, fill_value = 0)
    credit.constructor.print_vintage(cosechas_total)


def settings_cosecha():

    producto = 'credioficial'
    tipo_tasa = 'FIJA'
    frecuencia_reprecio = 0
    plazo = 36
    fecha_originacion = pd.to_datetime("2017-1-31")
    desembolso = 10000.0
    max_forecast = 120
    
    alturas_mora = [0, 30, 60, 90, 120, 150, 180, 210]
    
    vector_tasas_indice = pd.Series([0.0 * max_forecast], 
                                    index= alturas_mora)
    
    spread_originacion = interest_rates.models.fixed(max_forecast, 
                                                     fecha_originacion, 0.22)

    vector_prepago = credit.prepayment.psa(nper = max_forecast,
                                           ceil = 0.03,
                                           stable_per = 12)

    matrices_transicion = {1:[[0.9, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # 0
                              [0.0, 0.4, 0.6, 0.0, 0.0, 0.0, 0.0, 0.0],  # 30
                              [0.0, 0.0, 0.4, 0.6, 0.0, 0.0, 0.0, 0.0],  # 60
                              [0.0, 0.0, 0.0, 0.4, 0.6, 0.0, 0.0, 0.0],  # 90
                              [0.0, 0.0, 0.0, 0.0, 0.2, 0.8, 0.0, 0.0],  # 120
                              [0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.9, 0.0],  # 150
                              [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.9],  # 180
                              [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]]  # 210
                           }


    percent_prepago_por_calificacion = pd.Series([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                                                  index = alturas_mora)


    percent_recaudo_por_calificacion = pd.Series([1.0, 0.9, 0.7, 0.00, 0.0, 0.0, 0.0, 0.0],
                                                  index = alturas_mora)


    percent_castigo_por_calificacion = pd.Series([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
                                                  index = alturas_mora)


    percent_provision_por_calificacion = pd.Series([0.03, 0.035, 0.05, 0.10, 0.15, 0.25, 0.50, 1.0],
                                                  index = alturas_mora)

    settings = dict(producto = producto,
                    plazo = plazo,
                    tipo_tasa = tipo_tasa,
                    max_forecast = max_forecast,
                    alturas_mora = alturas_mora,
                    frecuencia_reprecio = frecuencia_reprecio,
                    fecha_originacion = fecha_originacion,
                    desembolso = desembolso,
                    vector_tasas_indice = vector_tasas_indice,
                    spread_originacion = spread_originacion,
                    vector_prepago = vector_prepago,
                    percent_prepago_por_calificacion = percent_prepago_por_calificacion,
                    matrices_transicion = matrices_transicion,
                    percent_recaudo_por_calificacion = percent_recaudo_por_calificacion,
                    percent_castigo_por_calificacion = percent_castigo_por_calificacion,
                    percent_provision_por_calificacion = percent_provision_por_calificacion,
                    )

    return settings


def correr_constructor_una_cosecha():
    settings = settings_cosecha()
    # pprint.pprint(settings)


    cosecha1 = constructor(settings)






if __name__ == '__main__':

    # correr_constructor_antiguo()
    correr_constructor_una_cosecha()
