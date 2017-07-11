import credit.prepayment
import rates.models
import pandas as pd
import definitions
import sqlite3
import credit.vintages as vintages
from common.presentation import tabulate_print


def get_contract_info(product_name):
    """
    Get contract info from forecast database
    :return: dict with nper, rate_type, repricing for a given product
    """
    # create tuple, for security reasons
    # https://docs.python.org/2/library/sqlite3.html
    p = (product_name,)

    # connect to database
    conn = sqlite3.connect(definitions.db_path())
    c = conn.cursor()

    # execute sql in db
    sql_sentence = "SELECT term, rate_type, repricing \
                            FROM contract_info WHERE \
                            product_name = ?"
    sql_ans = c.execute(sql_sentence, p)

    # fetch results
    ans = sql_ans.fetchall()

    # close cursor and db connection
    c.close()
    conn.close()

    return dict(nper=ans[0][0],
                rate_type = ans[0][1],
                repricing = ans[0][2])


def get_rolling_m(product_name):
    # connect to database
    conn = sqlite3.connect(definitions.db_path())
    c = conn.cursor()

    ans_dict = dict()
    for each_month in range(12):


        # execute sql in db
        sql_sentence = "SELECT _0, _30, _60, _90, _120, _150, _180 FROM credit \
        WHERE product_name = 'tarjeta de credito' and month = 1 \
        and score_id = 0"

        c.execute(sql_sentence)

        rolling_m = [[0.], [0.]]
        # update answer dictionary
        ans_dict[each_month + 1] = rolling_m

    # close cursor and db connection
    c.close()
    conn.close()

    return ans_dict


def get_forecast_info():
    pass


def vintage_settings():
    producto = 'tarjeta de credito'
    # tipo_tasa = 'FIJA'
    # frecuencia_reprecio = 0
    # plazo = 12
    fecha_originacion = pd.to_datetime("2017-1-31")
    desembolso = 10000.0
    forecast = 24
    alturas_mora = [0, 30, 60, 90, 120, 150, 180]
    tasas_indice = pd.Series(data = [0.0 * forecast],
                             index = alturas_mora)

    spreads = rates.models.fixed(nper = forecast,
                                 fecha_inicial = fecha_originacion,
                                 level = 0.22)

    prepago = credit.prepayment.psa(nper = forecast,
                                    ceil = 0.03,
                                    stable_per = 12)

    matrices_transicion = {
        'scores': [0, 30, 60, 90, 120, 150, 180],
        1: [[0.9, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.5, 0.1, 0.4, 0.0, 0.0, 0.0, 0.0],
            [0.3, 0.0, 0.1, 0.6, 0.0, 0.0, 0.0],
            [0.2, 0.0, 0.0, 0.2, 0.6, 0.0, 0.0],
            [0.1, 0.0, 0.0, 0.0, 0.1, 0.8, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.9],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3]]
    }

    per_prepago_cal = pd.Series(
            [1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0], index=alturas_mora)

    per_amor_calif = pd.Series(
            [1.0, 0.9, 0.7, 0.00, 0.0, 0.0, 0.0], index=alturas_mora)

    per_cast_calif = pd.Series(
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0], index=alturas_mora)

    settings = dict(name=producto,
                    forecast=forecast,
                    scores=alturas_mora,
                    sdate=fecha_originacion,
                    notional=desembolso,
                    tasas_indice=tasas_indice,
                    spreads=spreads,
                    prepago=prepago,
                    per_prepago_cal=per_prepago_cal,
                    matrices_transicion=matrices_transicion,
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

    print(get_rolling_m('tarjeta de credito'))

    #x1 = vintages.VintageForecast(vintage_settings())
    #print("Linea de negocio: ", x1.name())
    #print("Fecha de Originacion: ", x1.sdate())
    #print("Plazo de Originacion: ", x1.nper())
    #print("Tasas: ", x1.rate_type())
    #tabulate_print(x1.get_balance(per_score = False))
    #print(x1.get_serie(serie_name = 'saldo_inicial', per_score = False))

