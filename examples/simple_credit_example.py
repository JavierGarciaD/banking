from credit.prepayment import PrepaymentModel
from rates.models import InterestRateModel
import pandas as pd
import credit.vintages as vintages
from credit.forecast import vintage_settings
from credit.forecast import get_budget
from common.presentation import tabulate_print


if __name__ == '__main__':

    prod = 'tarjeta de credito'
    initial_date = '01-31-2017'

    budget = get_budget(product_name = prod, sdate = initial_date)
    fore = len(budget)

    prep_array = PrepaymentModel.psa(nper = fore,
                                     ceil = 0.03,
                                     stable_period = 12)

    index_array = InterestRateModel.zero(nper = fore,
                                         fecha_inicial = initial_date)

    ans = pd.DataFrame()
    for sdate, m_disbur in budget.iteritems():

        settings = vintage_settings(product_name = prod,
                                    sdate = sdate,
                                    disburment = m_disbur,
                                    fore_length = fore,
                                    prepay_array = prep_array,
                                    index_array =
                                    index_array)

        my_vintage = vintages.VintageForecast(settings = settings)
        print(sdate, ' - OK')

        ans = ans.add(my_vintage.get_balance(per_score = True),
                      fill_value = 0.0)
        #print("Linea de negocio: ", x1.name())
        #print("Fecha de Originacion: ", x1.sdate())
        #print("Plazo de Originacion: ", x1.nper())
        #print("Tasas: ", x1.rate_type())
        #tabulate_print(x1.
        #print(x1.get_serie(serie_name = 'saldo_inicial', per_score = False))
    print(ans)

