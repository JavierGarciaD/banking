import credit.prepayment
import rates.models
import pandas as pd
import credit.vintages as vintages
from credit.forecast import get_contract_info
from credit.forecast import get_scores
from credit.forecast import get_rolling
from common.presentation import tabulate_print


def vintage_settings():
    producto = 'tarjeta de credito'
    fecha_originacion = pd.to_datetime("2017-1-31")
    desembolso = 10000.0
    forecast = 24

    tasas_indice = pd.Series(data = [0.0 * forecast],
                             index = get_scores())

    spreads = rates.models.fixed(nper = forecast,
                                 fecha_inicial = fecha_originacion,
                                 level = 0.22)

    prepago = credit.prepayment.psa(nper = forecast,
                                    ceil = 0.03,
                                    stable_per = 12)

    per_prepago_cal = pd.Series(
            [1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0], index=get_scores())

    per_amor_calif = pd.Series(
            [1.0, 0.9, 0.7, 0.00, 0.0, 0.0, 0.0], index=get_scores())

    per_cast_calif = pd.Series(
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0], index=get_scores())

    settings = dict(name=producto,
                    forecast=forecast,
                    scores=get_scores(),
                    sdate=fecha_originacion,
                    notional=desembolso,
                    tasas_indice=tasas_indice,
                    spreads=spreads,
                    prepago=prepago,
                    per_prepago_cal=per_prepago_cal,
                    matrices_transicion=get_rolling(producto),
                    per_amor_calif=per_amor_calif,
                    per_cast_calif=per_cast_calif)

    # Gets information from forecast database about the contract:
    # nper, rate type, repricing frequency
    contract = get_contract_info(producto)

    # join two dictionaries, requires python 3.5
    # https://stackoverflow.com/questions/38987/how-to-merge-two-python-dictionaries-in-a-single-expression
    # https://www.python.org/dev/peps/pep-0448/
    return {**settings, **contract}


def provision_por_calificacion():
    return {0: 0.10,
            30: 0.15,
            60: 0.25,
            90: 0.40,
            120: 0.60,
            150: 0.80,
            180: 1.00
    }


if __name__ == '__main__':

    x1 = vintages.VintageForecast(vintage_settings())
    print("Linea de negocio: ", x1.name())
    print("Fecha de Originacion: ", x1.sdate())
    print("Plazo de Originacion: ", x1.nper())
    print("Tasas: ", x1.rate_type())
    tabulate_print(x1.get_balance(per_score = False))
    #print(x1.get_serie(serie_name = 'saldo_inicial', per_score = False))

