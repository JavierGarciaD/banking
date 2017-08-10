import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from credit.prepayment import PrepaymentModel
from rates.models import InterestRateModel
from credit.vintages import CreditVintage as CreditVintage
from common.presentation import tabulate_print as vint_print


def settings(name, forecast, nper, sdate, repricing, rate_type,
             rate_level, notional, scores, pay, prepay, w_off,
             rolling, credit_type):

    ans_dict = dict()

    ans_dict['name'] = name
    ans_dict['forecast'] = forecast
    ans_dict['nper'] = nper
    ans_dict['sdate'] = sdate
    ans_dict['repricing'] = repricing
    ans_dict['rate_type'] = rate_type
    ans_dict['notional'] = notional
    ans_dict['index_rates_array'] = InterestRateModel.zero(nper = forecast,
                                                           sdate = sdate)
    ans_dict['rate_spreads_array'] = InterestRateModel.fixed(nper = forecast,
                                                             sdate = sdate,
                                                             level =
                                                             rate_level)
    ans_dict['prepay_array'] = PrepaymentModel.psa(nper = forecast,
                                                   ceil = 0.03,
                                                   stable_period = 12)
    ans_dict['prepay_per_score'] = pd.Series(data = prepay, index = scores)
    ans_dict['rolling_m'] = rolling
    ans_dict['scores'] = scores
    ans_dict['pay_per_score'] = pd.Series(data = pay, index = scores)
    ans_dict['writeoff_per_score'] = pd.Series(data = w_off, index = scores)
    ans_dict['credit_type'] = credit_type

    return ans_dict


if __name__ == '__main__':
    roll = [[0.97, 0.03, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
            [0.40, 0.05, 0.55, 0.00, 0.00, 0.00, 0.00, 0.00],
            [0.16, 0.02, 0.02, 0.80, 0.00, 0.00, 0.00, 0.00],
            [0.03, 0.00, 0.00, 0.03, 0.94, 0.00, 0.00, 0.00],
            [0.00, 0.00, 0.00, 0.01, 0.01, 0.98, 0.00, 0.00],
            [0.01, 0.00, 0.00, 0.00, 0.03, 0.02, 0.94, 0.00],
            [0.05, 0.00, 0.00, 0.00, 0.00, 0.00, 0.05, 0.90],
            [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 1.00]]

    sett = settings(name = 'credioficial',
                    nper = 96,
                    credit_type = 'consumer',
                    sdate = '31-01-2016',
                    forecast = 60,
                    repricing = 0,
                    rate_type = 'FIX',
                    rate_level = 0.2,
                    notional = 10000.0,
                    scores = [0, 30, 60, 90, 120, 150, 180, 210],
                    pay = [0.99, 0.75, 0.55, 0.23, 0.15, 0.05, 0.01, 0.0],
                    prepay = [1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    w_off = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.5],
                    rolling = {1: roll}
                    )

    charting = True

    vintage = CreditVintage(settings = sett)

    print(vintage.name())
    vint_print(vintage.get_balance(per_score = False))

    npl = vintage.get_quality(result = 'nonperforming', type = 'abs')

    # charting
    if charting:
        matplotlib.style.use('ggplot')
        npl.plot(title = 'Cartera Vencida', linewidth=5.0)
        plt.show()
