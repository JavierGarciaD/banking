

import credit.constructor
import credit.constructor_cosechas as constructor
import credit.prepayment
import interest_rates.models

import pprint



def correr_constructor_antiguo():
    proyeccion = 60
    producto = 'pyme'
    plazo = 24
    tasas = interest_rates.models.fixed(plazo, 0.0145)
    prepago = credit.prepayment.psa(nper = plazo, ceil = 0.03, stable_per = 12)

    modelo_credito = credit.constructor.CreditModel.simple(nper = plazo,
                                                           loss = 0.02)
    presupuesto = [20000] * proyeccion

    cont_conditions = dict(balance = 0.0,
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
    tipo_tasa = 'fija'
    frecuencia_reprecio = 0
    plazo = 36
    fecha_originacion = "2017-1-31"
    desembolso = 10000.0

    vector_tasas_indice = [.0] * plazo
    tasa_originacion = interest_rates.models.fixed(plazo, 0.0134)
    vector_prepago = credit.prepayment.psa(
        nper = plazo, ceil = 0.03, stable_per = 12)

    matrices_transicion = {1:[[0.9, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # 0
                              [0.0, 0.4, 0.6, 0.0, 0.0, 0.0, 0.0, 0.0],  # 30
                              [0.0, 0.0, 0.4, 0.6, 0.0, 0.0, 0.0, 0.0],  # 60
                              [0.0, 0.0, 0.0, 0.4, 0.6, 0.0, 0.0, 0.0],  # 90
                              [0.0, 0.0, 0.0, 0.0, 0.2, 0.8, 0.0, 0.0],  # 120
                              [0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.9, 0.0],  # 150
                              [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.9],  # 180
                              [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]]  # 210
                           }

    recaudo_por_calificacion = {0:1.0,
                                30:1.0,
                                60:0.90,
                                90:0.80,
                                120:0.70,
                                150:0.0,
                                180:0.0,
                                210:0.0}

    castigo_por_calificacion = {0:0.0,
                                30:0.0,
                                60:0.0,
                                90:0.0,
                                120:0.0,
                                150:0.0,
                                180:0.0,
                                210:1.0}

    provision_por_calificacion = {0:0.03,
                                  30:0.035,
                                  60:0.05,
                                  90:0.1,
                                  120:0.15,
                                  150:0.25,
                                  180:0.50,
                                  210:1.0}

    settings = dict(producto = producto,
                    plazo = plazo,
                    tipo_tasa = tipo_tasa,
                    frecuencia_reprecio = frecuencia_reprecio,
                    fecha_originacion = fecha_originacion,
                    desembolso = desembolso,
                    vector_tasas_indice = vector_tasas_indice,
                    tasa_originacion = tasa_originacion,
                    vector_prepago = vector_prepago,
                    matrices_transicion = matrices_transicion,
                    recaudo_por_calificacion = recaudo_por_calificacion,
                    castigo_por_calificacion = castigo_por_calificacion,
                    provision_por_calificacion = provision_por_calificacion,
                    )

    return settings


def correr_constructor_una_cosecha():
    settings = settings_cosecha()
    # pprint.pprint(settings)


    cosecha1 = constructor(settings)






if __name__ == '__main__':

    # correr_constructor_antiguo()
    correr_constructor_una_cosecha()
