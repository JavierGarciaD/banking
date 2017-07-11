import numpy as np
import pandas as pd
from banking.common.presentation import tabulate_print
from examples.simple_credit_example import settings_cosecha
from rates.conversion import ea_a_nmv
from rates.conversion import compound_effective_yr


class CreditVintage:

    #############################################################
    # Private methods
    #############################################################

    def __init__(self, settings):
        """
        :return an object with information for a loan portfolio on
        an homogeneous loan pool, where the loans share the same origination
        period.
        """
        self._dec = 2
        self._forecast = settings['forecast']

        self._name = settings['name']
        self._nper = settings['nper']
        self._sdate = pd.to_datetime(settings['sdate'])
        self._notional = np.round(settings['notional'], self._dec)

        self._repricing = settings['repricing']
        self._rate_type = settings['rate_type']
        self._index_vals = np.round(settings['tasas_indice'], 6)
        self._spreads = np.round(settings['spreads'], 6)

        self._prepay = settings['prepago']
        self._prepay_score = settings['per_prepago_cal']

        self._rolling_m = settings['matrices_transicion']
        self._scores = settings['matrices_transicion']['scores']
        self._pay_calif = settings['per_amor_calif']
        self._write_off = settings['per_cast_calif']

        ##########################################################
        # building  structures
        ##########################################################

        # cols orders must be preserved
        self._cols = ['saldo_inicial', 'desembolso', 'amortizacion', 'prepago',
                      'castigo', 'saldo_final']

        self.ans_df = self._df_structure()
        self.temp_struc = self._term_structure()
        self.tasas_nmv = self._nominal_rates()

        ##########################################################
        # initialize the balance
        ##########################################################
        self._balance_constructor()

    def _balance_constructor(self):
        """
        Construct a dataframe with projections of balances for
        a loan portfolio in an homogeneous loan pool, where the loans share
        the same origination period.

        :return: dataframe
        """
        disbu = self._cols[1] + '_' + str(0)

        for row, _col in self.ans_df.iterrows():
            # T+0 disbursement
            if row == self._sdate:
                self.ans_df.loc[self._sdate, disbu] = self._notional
            self._prepay_update_row(row)
            self._write_off_update_row(row)
            self._pay_update_row(row)
            self._end_update_row(row)
            self._initial_update_row(row)

        return self.ans_df

    def _df_structure(self):
        """
        Creates output df structure
        """
        cols = [each_col + "_" + str(each_score) for each_col in self._cols
                for each_score in self._scores]

        dates_index = pd.date_range(start = self._sdate,
                                    periods = self._forecast, freq = 'M')

        return pd.DataFrame(data = 0.0, index = dates_index, columns = cols)

    def _initial_update_row(self, row):
        """
        Update initial balance given an end balance and a rolling matrix
        """
        end_bal_with_trans = self._apply_transition(row)
        if row + 1 <= self.ans_df.index[-1]:
            for each_score in self._scores:
                col = self._cols[0] + '_' + str(each_score)
                ans = end_bal_with_trans.get_value(each_score)
                self.ans_df.loc[row + 1, col] = np.round(ans, self._dec)

    def _end_update_row(self, row):
        """
        Update end balance
        End Balance = Initial balance + Disbursement - Contractual payment -
        Prepayment - WriteOff
        """
        # ['saldo_inicial', 'desembolso', 'amortizacion', 'prepago',
        #              'castigo', 'saldo_final']
        for each_score in self._scores:
            i_b = self._cols[0] + '_' + str(each_score)
            dis = self._cols[1] + '_' + str(each_score)
            pay = self._cols[2] + '_' + str(each_score)
            pre = self._cols[3] + '_' + str(each_score)
            w_o = self._cols[4] + '_' + str(each_score)
            e_b = self._cols[5] + '_' + str(each_score)

            ans = (self.ans_df.loc[row, i_b]
                   + self.ans_df.loc[row, dis]
                   - self.ans_df.loc[row, pay]
                   - self.ans_df.loc[row, pre]
                   - self.ans_df.loc[row, w_o])
            self.ans_df.loc[row, e_b] = np.round(ans, self._dec)

    def _prepay_update_row(self, row):
        """
        Computes prepayment as initial balance times prepayment by score times
        prepayment by age
        Update output df
        """
        prepay_per_age = self._prepay[self.ans_df.index.get_loc(row)]
        a = self._prepay_score * prepay_per_age
        b = self._get_data_by_row(row, self._cols[0])  # initial balance
        c = a * b
        for each_score in self._scores:
            col = self._cols[3] + '_' + str(each_score)
            ans = c.get_value(each_score)
            self.ans_df.loc[row, col] = np.round(ans, self._dec)

    def _pay_update_row(self, row):
        """
        Computes contractual payments for a credit
        """
        k = self.temp_struc[row] * self._notional
        i = self.tasas_nmv.get_value(row)
        per = row.to_period('M') - self._sdate.to_period('M')

        # computes contractual payment for each score
        ans = pd.Series(0.0, index = self._scores)
        for index, val in k.iteritems():
            # capital payment for each score
            if 0 < per <= self._nper:
                ppay = np.abs(np.ppmt(i, per, self._nper, val, 0))
                ppay = np.round(self._dec, ppay * self._pay_calif[index])
                ans.set_value(index, ppay)
            # After the initial term of the credit any value that because
            # rolling goes to score 0 goes to amortization of capital
            elif per > self._nper and index == 0:
                ans.set_value(index,
                              self.ans_df.loc[row, self._cols[0] + '_0'])

        # Update ans_df
        for each_score in self._scores:
            i_b = self._cols[0] + '_' + str(each_score)
            pay = self._cols[2] + '_' + str(each_score)
            pre = self._cols[3] + '_' + str(each_score)
            w_o = self._cols[4] + '_' + str(each_score)

            net_pay = min((self.ans_df.loc[row, i_b]
                           - self.ans_df.loc[row, pre]
                           - self.ans_df.loc[row, w_o]),
                          ans.get(each_score))

            self.ans_df.loc[row, pay] = np.round(net_pay, self._dec)

    def _write_off_update_row(self, row):
        """
        Computes the write off value for each score as initial balance times
        write off by score
        Update output df
        """
        a = self._write_off
        b = self._get_data_by_row(row, self._cols[0])  # initial balance
        c = a * b

        for each_score in self._scores:
            col = self._cols[4] + '_' + str(each_score)
            ans = c.get_value(each_score)
            self.ans_df.loc[row, col] = np.round(ans, self._dec)

    def _term_structure(self):
        """
        :return dictionary with term structure of a vintage given a rolling
        matriz for each period.
        """
        ans_dict = dict.fromkeys(pd.date_range(self._sdate,
                                               periods = self._forecast,
                                               freq = 'M'))

        for key in sorted(ans_dict.keys()):
            if key == sorted(ans_dict.keys())[0]:
                ans0 = pd.Series(0.0, index = self._scores)
                ans0[0, 0] = 1.0
                ans_dict[key] = ans0
            else:
                m = self._get_rolling_m(key)
                ans = np.dot(np.transpose(m), ans_dict[key - 1])
                ans_dict[key] = pd.Series(ans, index = self._scores)
        return ans_dict

    def _nominal_rates(self):
        """
        :return Pandas Series of nominal periodic rates adjusted by repricing
        frequency
        """
        if self._rate_type == "FIJA":
            return np.round(ea_a_nmv(vector_a = self._spreads), self._dec)

        elif self._rate_type == "DTF" or self._rate_type == "IPC":
            ea = compound_effective_yr(repriced_spread = self._index_vals,
                                       fixed_spreads = self._spreads,
                                       repricing = self._repricing)
            return np.round(ea_a_nmv(vector_a = ea), 6)

        elif self._rate_type == "IBR":
            raise NotImplementedError

    def _get_rolling_m(self, row):
        """
        :return the transition matrix for the period. If a correct matrix is
        not found, look up for month = 1 else keyerror
        """
        if row.month > 12:
            raise KeyError('Month {} does not exist: '.format(str(row.month)))
        elif row.month in self._rolling_m.keys():
            return self._rolling_m[row.month]
        else:
            return self._rolling_m[1]

    def _apply_transition(self, row):
        """
        Apply a transition matrix to a vector of balances for delinquency,
        """
        m = self._get_rolling_m(row)
        end_bal = self._get_data_by_row(row, self._cols[-1])
        ans = np.dot(np.transpose(m), end_bal)
        return pd.Series(ans, index = self._scores)

    def _get_data_by_row(self, row, data):
        """
        :return Pandas Serie with the balance for a data type by score,
        for a given date (row)
        """
        data_pos = self._cols.index(data)
        cols = [self._cols[data_pos] + '_' + str(each_score) for each_score in
                self._scores]
        ans = [self.ans_df.loc[row, each_col] for each_col in cols]

        return pd.Series(ans, index = self._scores)

    #############################################################
    # Public methods
    #############################################################

    def name(self):
        """
        :return: str linea de negocio
        """
        return self._name

    def nper(self):
        """
        :return: int
        """
        return self._nper

    def sdate(self):
        """
        :return: date
        """
        return self._sdate

    def rate_type(self):
        """
        :return: list [tipo tasa, valor]
        """
        return [self._rate_type, self._spreads[0]]

    def get_balance(self, per_score = False):
        """

        """
        if per_score:
            return self.ans_df
        else:
            ans = pd.DataFrame(columns = self._cols, index = self.ans_df.index)
            for col in ans:
                ans[col] = self.get_serie(serie_name = col, per_score = False)
            return ans

    def get_serie(self, serie_name, per_score = False):
        serie_name = serie_name.lower()
        cols_names = [serie_name + '_' + str(each_score) for each_score in
                      self._scores]
        ans = self.ans_df[cols_names]

        if per_score:
            return ans
        else:
            return ans.sum(axis = 1).rename(serie_name)

    def get_index(self):
        """
        Retorna el indice de fechas de la cosecha
        """
        return self.ans_df.index


if __name__ == '__main__':
    from pprint import pprint
    x1 = CreditVintage(settings_cosecha())
    print("Linea de negocio: ", x1.name())
    print("Fecha de Originacion: ", x1.sdate())
    print("Plazo de Originacion: ", x1.nper())
    print("Tasas: ", x1.rate_type())
    tabulate_print(x1.get_balance(per_score = False))
    #print(x1.get_serie(serie_name = 'saldo_inicial', per_score = False))

