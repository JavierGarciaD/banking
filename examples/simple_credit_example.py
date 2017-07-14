from credit.prepayment import PrepaymentModel
from rates.models import InterestRateModel
import pandas as pd
import credit.vintages as vintages
from credit.forecast import get_contract_info
from credit.forecast import get_scores
from credit.forecast import get_rolling
from credit.forecast import get_budget
from common.presentation import tabulate_print


def vintage_settings(product_name, sdate,
                     disburment, fore_length,
                     prepay_array, index_array):

    # Gets information from forecast database about the contract_info:
    # nper, rate type, repricing frequency
    contract_info = get_contract_info(product_name)

    # spread over index is fixed
    spreads_array = InterestRateModel.fixed(nper = fore_length,
                                            sdate = sdate,
                                            level = contract_info[
                                                'rate_spread'])

    settings = dict(name = product_name,
                    nper = contract_info['nper'],
                    rate_type = contract_info['rate_type'],
                    repricing = contract_info['repricing'],
                    forecast = int(fore_length),
                    scores = get_scores(),
                    sdate = pd.to_datetime(sdate),
                    notional = float(disburment),
                    index_rates_array = index_array,
                    rate_spreads_array=spreads_array,
                    prepay_array=prepay_array,
                    prepay_per_score=contract_info['prepay_per_score'],
                    rolling_m=get_rolling(product_name),
                    pay_per_score=contract_info['pay_per_score'],
                    writeoff_per_score=contract_info['writeoff_per_score']
                    )

    return settings


# def provision_por_calificacion():
#     return {0: 0.10,
#             30: 0.15,
#             60: 0.25,
#             90: 0.40,
#             120: 0.60,
#             150: 0.80,
#             180: 1.00
#     }


if __name__ == '__main__':

    prod = 'tarjeta de credito'
    my_date = '01-31-2017'

    budget = get_budget(prod, my_date)

    month_disburtment = budget[0]
    fore = len(budget)

    prep_array = PrepaymentModel.psa(nper = fore,
                                     ceil = 0.03,
                                     stable_period = 12)

    index_array = InterestRateModel.zero(nper = fore,
                                         fecha_inicial = my_date)

    x1 = vintages.VintageForecast(vintage_settings(product_name = prod,
                                                   sdate = my_date,
                                                   disburment = month_disburtment,
                                                   fore_length = fore,
                                                   prepay_array = prep_array,
                                                   index_array = index_array))

    print("Linea de negocio: ", x1.name())
    print("Fecha de Originacion: ", x1.sdate())
    print("Plazo de Originacion: ", x1.nper())
    print("Tasas: ", x1.rate_type())
    tabulate_print(x1.get_balance(per_score = False))
    #print(x1.get_serie(serie_name = 'saldo_inicial', per_score = False))

