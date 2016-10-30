

import numpy as np
import pandas as pd


class CreditModel:
    """

    """

    def __init__(self):
        pass

    @staticmethod
    def zero(nper):
        return dict(loss=[0.0] * nper,
                    nonperforming=[0.0] * nper,
                    provision=[0.0] * nper)

    @staticmethod
    def simple(nper, loss=0.02,
               nonperforming=0.03,
               provision=0.035):
        return dict(loss=[loss] * nper,
                    nonperforming=[nonperforming] * nper,
                    provision=[provision] * nper)


class CreditVintage:
    """
    Construct an object with information for a loan portfolio on
    an homogeneous loan pool, where the loans share the same origination period.
    """

    def __init__(self, settings):
        """Init
        """
        self._product_name = settings['name']
        self._origination = settings['origination']
        self._origination_month = settings['month']
        self._rates_vector = settings['rates_vector']
        self._nper = settings['nper']
        self._prepayment_vector = settings['prepayment_vector']
        self._credit_model = settings['credit_model']

    def product_name(self):
        """
        :return: str name of credit product
        """
        return self._product_name

    def origination_month(self):
        """
        :return: int moth of origination
        """
        return self._origination_month

    def origination(self):
        """
        :return: float origination value of vintage
        """
        return self._origination

    def nper(self):
        """
        :return: int number of periods
        """
        return self._nper

    def rates_vector(self):
        """
        :return: list with rates used
        """
        return self._rates_vector

    def prepayment_vector(self):
        """
        :return: list with prepayment rates used
        """
        return self._prepayment_vector

    def credit_model(self):
        """
        :return: dict with credit assumptions
        """
        return self._credit_model

    def cashflows_old(self):
        """
        Construct a dataframe with projections of balances and cashflows for a loan portfolio
        in an homogeneous loan pool, where the loans share the same origination period.
        :rtype: pandas dataframe
        """
        loss_rates = self._credit_model.get('castigo')
        nonperforming_rates = self._credit_model.get('improductiva')
        provision_rates = self._credit_model.get('provision')
        prepayment_rates = self._prepayment_vector
        rates = self._rates_vector

        ans_df = pd.DataFrame(0., index=range(self._nper), columns=('saldo_inicial',
                                                                    'desembolsos',
                                                                    'amortizacion',
                                                                    'prepago',
                                                                    'castigo',
                                                                    'saldo_final',
                                                                    'interes',
                                                                    'improductiva',
                                                                    'saldo_provision'))
        ans_df.loc[0] = [0,
                         self._origination,
                         0,
                         0,
                         0,
                         self._origination,
                         0,
                         0,
                         self._origination * provision_rates[0]]

        rounding = 6
        min_balance = 0.01
        initial_balance = self._origination
        for payment in range(self._nper):
            index = payment + 1
            loss = np.round(initial_balance * loss_rates[payment], rounding)
            prepayment = np.round(
                initial_balance * prepayment_rates[payment], rounding)
            nonperforming = np.round(
                initial_balance * nonperforming_rates[payment], rounding)
            provision = np.round(
                (provision_rates[payment] * (initial_balance - nonperforming)) + nonperforming)
            ipmt = np.round(
                (initial_balance - nonperforming) * rates[payment], rounding)

            contractual_ppmt = np.round(
                -(np.ppmt(rates[payment], index, self._nper, self._origination)), rounding)
            if contractual_ppmt > (initial_balance - prepayment - loss):
                ppmt = np.round(initial_balance - prepayment - loss, rounding)
            else:
                ppmt = contractual_ppmt

            ending_balance = np.round(
                initial_balance - ppmt - prepayment - loss, rounding)
            if ending_balance < min_balance:
                ending_balance = 0.

            origination = np.round(0., rounding)
            if index == 0:
                origination = np.round(self._origination, rounding)

            ans_df.loc[index] = [initial_balance,
                                 origination,
                                 ppmt,
                                 prepayment,
                                 loss,
                                 ending_balance,
                                 ipmt,
                                 nonperforming,
                                 provision]

            initial_balance = ending_balance
        return ans_df

    def cashflows(self):
        """
        Construct a dataframe with projections of balances and cashflows for a loan portfolio
        in an homogeneous loan pool, where the loans share the same origination period.
        :rtype: pandas dataframe
        """
        loss_rates = self._credit_model.get('loss')
        nonperforming_rates = self._credit_model.get('nonperforming')
        provision_rates = self._credit_model.get('provision')
        prepayment_rates = self._prepayment_vector
        rates = self._rates_vector
        index_to_apply = list(
            range(self.origination_month(), self.origination_month() + self._nper + 1))

        ans_df = pd.DataFrame(0.,
                              index=index_to_apply,
                              columns=('saldo_inicial',
                                       'desembolsos',
                                       'amortizacion',
                                       'prepago',
                                       'castigo',
                                       'saldo_final',
                                       'interes',
                                       'improductiva',
                                       'saldo_provision'))

        ans_df.loc[self.origination_month()] = [0,
                                                self._origination,
                                                0,
                                                0,
                                                0,
                                                self._origination,
                                                0,
                                                0,
                                                self._origination * provision_rates[0]]

        rounding = 6
        min_balance = 0.01
        initial_balance = self._origination
        for payment in range(self._nper):
            index = payment + self.origination_month()
            loss = np.round(initial_balance * loss_rates[payment], rounding)
            prepayment = np.round(
                initial_balance * prepayment_rates[payment], rounding)
            nonperforming = np.round(
                initial_balance * nonperforming_rates[payment], rounding)
            provision = np.round((provision_rates[payment] * (initial_balance - nonperforming)) + nonperforming,
                                 rounding)
            ipmt = np.round(
                (initial_balance - nonperforming) * rates[payment], rounding)

            contractual_ppmt = np.round(-(np.ppmt(rates[payment],
                                                  payment + 1, self._nper, self._origination)), rounding)
            if contractual_ppmt > (initial_balance - prepayment - loss):
                ppmt = np.round(initial_balance - prepayment - loss, rounding)
            else:
                ppmt = contractual_ppmt

            ending_balance = np.round(
                initial_balance - ppmt - prepayment - loss, rounding)
            if ending_balance < min_balance:
                ending_balance = 0.

            origination = np.round(0., rounding)

            ans_df.loc[index + 1] = [initial_balance,
                                     origination,
                                     ppmt,
                                     prepayment,
                                     loss,
                                     ending_balance,
                                     ipmt,
                                     nonperforming,
                                     provision]

            initial_balance = ending_balance
        return ans_df

    def saldo_inicial(self):
        """
        :return: initial balance at each point in time for vintage as pandas series
        """
        cashflows = self.cashflows()
        return cashflows['saldo_inicial']

    def improductiva(self):
        """
        :return: nonperforming loans time series as pandas series
        """
        cashflows = self.cashflows()
        return cashflows['improductiva']

    def amortizacion(self):
        """
        :return: repayment schedule as pandas series
        """
        cashflows = self.cashflows()
        return cashflows['amortizacion']

    def prepago(self):
        """
        :return: prepayment at each point in time for vintage as pandas series
        """
        cashflows = self.cashflows()
        return cashflows['prepago']

    def castigo(self):
        """
        :return: credit loss at each point in time for vintage as pandas series
        """
        cashflows = self.cashflows()
        return cashflows['castigo']

    def saldo_final(self):
        """
        :return: ending balance at each point in time for vintage as pandas series
        """
        cashflows = self.cashflows()
        return cashflows['saldo_final']

    def interes(self):
        """
        :return: interest payment at each point in time for vintage as pandas series
        """
        cashflows = self.cashflows()
        return cashflows['interes']

    def saldo_provision(self):
        """
        :return: provision balance at each point in time for vintage as pandas series
        """
        cashflows = self.cashflows()
        return cashflows['saldo_provision']


def contractual_vintage(contractual_conditions, prepayment_rates, credit_model, out_to=None):
    loss_rates = credit_model.get('loss')
    nonperforming_rates = credit_model.get('nonperforming')
    provision_rates = credit_model.get('provision')
    fixed_rate = contractual_conditions.get('fixed_rate')
    ppmt = contractual_conditions.get('ppmt')
    # spread_DTF = contractual_conditions.get('spread_DTF')
    # spread_IBR = contractual_conditions.get('spread_IBR')
    # repricing = contractual_conditions.get('repricing')

    index_to_apply = list(range(len(ppmt)))
    ans_df = pd.DataFrame(0.,
                          index=index_to_apply,
                          columns=('saldo_inicial',
                                   'desembolsos',
                                   'amortizacion',
                                   'prepago',
                                   'castigo',
                                   'saldo_final',
                                   'interes',
                                   'improductiva',
                                   'saldo_provision'))

    rounding = 6
    min_balance = 0.1
    initial_balance = contractual_conditions.get('balance')
    origination = 0
    for key in range(len(ans_df)):
        if key == 0:
            ans_df['saldo_inicial'] = np.round(
                contractual_conditions.get('balance'), rounding)

        loss = np.round(initial_balance * loss_rates[key], rounding)
        prepayment = np.round(
            initial_balance * prepayment_rates[key], rounding)
        nonperforming = np.round(
            initial_balance * nonperforming_rates[key], rounding)
        provision = np.round(
            (provision_rates[key] * (initial_balance - nonperforming)) + nonperforming, rounding)
        ipmt = np.round(
            (initial_balance - nonperforming) * fixed_rate[key], rounding)

        contractual_ppmt = np.round(
            contractual_conditions.get('ppmt')[key], rounding)
        if contractual_ppmt > (initial_balance - prepayment - loss):
            ppmt = np.round(initial_balance - prepayment - loss, rounding)
        else:
            ppmt = contractual_ppmt

        ending_balance = np.round(
            initial_balance - ppmt - prepayment - loss, rounding)
        if ending_balance < min_balance:
            ending_balance = 0.

        ans_df.loc[key] = [initial_balance,
                           origination,
                           ppmt,
                           prepayment,
                           loss,
                           ending_balance,
                           ipmt,
                           nonperforming,
                           provision]

        initial_balance = ending_balance

    if out_to is None:
        return ans_df
    else:
        print_vintage(ans_df)


def vintage_settings(name, term, month, origination, rates, prepayment, credit_model):
    """Settings for creating a vintage object
    :return: dict
    """

    return dict(name=name,
                month=month,
                origination=origination,
                nper=term,
                rates_vector=rates,
                prepayment_vector=prepayment,
                credit_model=credit_model)


def collection_of_vintages(name, length_of_projection, term, rates, prepayment, credit_model, budget,
                           out_to="consolidate"):
    """

    :return: dict of dicts
    """
    ans = dict()
    for each_month in range(length_of_projection):
        settings = vintage_settings(name,
                                    term,
                                    each_month,
                                    budget[each_month],
                                    rates,
                                    prepayment,
                                    credit_model)
        ans[each_month] = CreditVintage(settings)

    if out_to is "each":
        return ans
    elif out_to == "each print":
        for __, value in ans.items():
            print_vintage(value.cashflows())
    elif out_to == "consolidate":
        return consolidation(ans)
    elif out_to == "consolidate print":
        print_consolidation(ans)


def consolidation(collection):

    length = len(collection)
    term = collection[0].nper()
    ans_df = pd.DataFrame(0., index=range(term + length), columns=('saldo_inicial',
                                                                   'desembolsos',
                                                                   'amortizacion',
                                                                   'prepago',
                                                                   'castigo',
                                                                   'saldo_final',
                                                                   'interes',
                                                                   'improductiva',
                                                                   'saldo_provision'))
    for each_vintage in collection:
        ans_df = ans_df.add(collection[each_vintage].cashflows(), fill_value=0)

    return ans_df


def print_consolidation(collection):
    from tabulate import tabulate
    print(tabulate(consolidation(collection),
                   headers='keys',
                   numalign='right',
                   tablefmt='psql',
                   floatfmt=",.0f"))


def print_vintage(vintage):
    """
    Print nicely the vintage results
    :param vintage: credit vintage object
    :return: console output
    """
    from tabulate import tabulate
    print(tabulate(vintage,
                   headers='keys',
                   numalign='right',
                   tablefmt='psql',
                   floatfmt=",.0f"))
