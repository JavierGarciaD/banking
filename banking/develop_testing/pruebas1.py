

import credit.prepago
import interest_rates.models
import pandas as pd




def settings_cosecha():

    producto = 'credioficial'
    tipo_tasa = 'FIJA'
    frecuencia_reprecio = 0
    plazo = 12
    fecha_originacion = pd.to_datetime("2017-1-31")
    desembolso = 10000.0
    max_forecast = plazo*2

    alturas_mora = [0, 30, 60, 90, 120, 150, 180, 210]

    vector_tasas_indice = pd.Series([0.0 * max_forecast],
                                    index = alturas_mora)

    spread_originacion = interest_rates.models.fixed(max_forecast,
                                                     fecha_originacion, 
                                                     0.22)

    vector_prepago = credit.prepago.psa(nper = max_forecast,
                                           ceil = 0.03,
                                           stable_per = 12)


    matrices_transicion = {1:[[0.9, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # 0
                              [0.5, 0.1, 0.4, 0.0, 0.0, 0.0, 0.0, 0.0],  # 30
                              [0.3, 0.0, 0.1, 0.6, 0.0, 0.0, 0.0, 0.0],  # 60
                              [0.2, 0.0, 0.0, 0.2, 0.6, 0.0, 0.0, 0.0],  # 90
                              [0.1, 0.0, 0.0, 0.0, 0.1, 0.8, 0.0, 0.0],  # 120
                              [0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.9, 0.0],  # 150
                              [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3, 0.7],  # 180
                              [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]]  # 210
                           }


    percent_prepago_por_calificacion = pd.Series([1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                                                  index = alturas_mora)


    percent_recaudo_por_calificacion = pd.Series([1.0, 0.9, 0.7, 0.00, 0.0, 0.0, 0.0, 0.0],
                                                  index = alturas_mora)


    percent_castigo_por_calificacion = pd.Series([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
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
                    percent_castigo_por_calificacion = percent_castigo_por_calificacion)
                    
    return settings


def provision_por_calificacion():
    
    return {0 : 0.10,
            30 : 0.15,
            60 : 0.25,
            90 : 0.40,
            120 : 0.60,
            150 : 0.80,
            180 : 0.90,
            210 : 1.00}
    
    