import credit.prepayment
import rates.models
import pandas as pd
import numpy as np


def settings_cosecha():
    producto = 'credioficial'
    tipo_tasa = 'FIJA'
    frecuencia_reprecio = 0
    plazo = 12
    fecha_originacion = pd.to_datetime("2017-1-31")
    desembolso = 10000.0
    forecast = plazo * 2
    alturas_mora = [0, 30, 60, 90, 120, 150, 180, 210]
    tasas_indice = pd.Series(data = [0.0 * forecast],
                             index = alturas_mora)

    spreads = rates.models.fixed(nper = forecast,
                                 fecha_inicial = fecha_originacion,
                                 level = 0.22)

    prepago = credit.prepayment.psa(nper = forecast,
                                    ceil = 0.03,
                                    stable_per = 12)

    matrices_transicion = {
        'scores': [0, 30, 60, 90, 120, 150, 180, 210],
        1: [[0.9, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.5, 0.1, 0.4, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.3, 0.0, 0.1, 0.6, 0.0, 0.0, 0.0, 0.0],
            [0.2, 0.0, 0.0, 0.2, 0.6, 0.0, 0.0, 0.0],
            [0.1, 0.0, 0.0, 0.0, 0.1, 0.8, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.9, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3, 0.7],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]]
    }

    per_prepago_cal = pd.Series(
            [1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], index=alturas_mora)

    per_amor_calif = pd.Series(
            [1.0, 0.9, 0.7, 0.00, 0.0, 0.0, 0.0, 0.0], index=alturas_mora)

    per_cast_calif = pd.Series(
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0], index=alturas_mora)

    settings = dict(name=producto, nper=plazo, rate_type=tipo_tasa,
                    forecast=forecast, scores=alturas_mora,
                    repricing=frecuencia_reprecio,
                    sdate=fecha_originacion, notional=desembolso,
                    tasas_indice=tasas_indice,
                    spreads=spreads,
                    prepago=prepago,
                    per_prepago_cal=per_prepago_cal,
                    matrices_transicion=matrices_transicion,
                    per_amor_calif=per_amor_calif,
                    per_cast_calif=per_cast_calif)

    return settings


def provision_por_calificacion():
    return {0:   0.10, 30: 0.15, 60: 0.25, 90: 0.40, 120: 0.60, 150: 0.80, 180: 0.90,
            210: 1.00}
