import numpy as np
import pandas as pd
from banking.common.presentation import print_tabulate
from examples.simple_credit_example import settings_cosecha


class Cosecha_Credito:
    def __init__(self, settings):
        """
        Construct an object with information for a loan portfolio on
        an homogeneous loan pool, where the loans share the same origination
        period.
        """
        self._dec = 2
        self._forecast = settings['forecast']

        self._name = settings['name']
        self._nper = settings['nper']
        self._sdate = pd.to_datetime(settings['sdate'])
        self._notional = np.round(settings['notional'], self._dec)

        self._scores = settings['scores']

        self._repricing = settings['repricing']
        self._rate_type = settings['rate_type']
        self._index_vals = np.round(settings['tasas_indice'], 6)
        self._spreads = np.round(settings['spreads'], 6)

        self._prepay = settings['prepago']
        self._prepay_score = settings['per_prepago_cal']

        self._rolling_m = settings['matrices_transicion']
        self._pay_calif = settings['per_amor_calif']
        self._write_off = settings['per_cast_calif']

        ##########################################################
        # building  structures
        ##########################################################

        # cols orders must be preserved
        self._cols = ['saldo_inicial', 'desembolso', 'amortizacion', 'prepago',
                      'castigo', 'saldo_final']

        self.ans_df = self._df_structure()
        self.temp_struc = self._temp_structure()
        self.tasas_nmv = self._tasas_full_nmv()

        ##########################################################
        # initialize the balance
        ##########################################################
        self._balance()

    def _balance(self):
        """
        Construct a dataframe with projections of balances for
        a loan portfolio in an homogeneous loan pool, where the loans share
        the same origination period.

        :return: dataframe
        """
        x = self._cols[1] + '_' + str(0)
        # row by row
        for row, _col in self.ans_df.iterrows():

            # T+0 disbursement
            if row == self._sdate:
                self.ans_df.loc[self._sdate, x] = self._notional
            self._prepay_update_row(row)
            self._write_off_update_row(row)
            self._pay_update_row(row)
            self._end_update_row(row)
            self._apply_transition(row)

        return self.ans_df

    def _df_structure(self):
        """
        Creates output df structure

        """
        cols = [each_col + "_" + str(each_score) for each_col in self._cols
                for each_score in self._rolling_m['scores']]
        dates_index = pd.date_range(self._sdate,
                                    periods = self._forecast,
                                    freq = 'M')
        return pd.DataFrame(0.0, index = dates_index, columns = cols)

    def _initial_update_row(self, row, end_bal_with_trans):
        """
        Update initial balance given an end balance
        """

        for each_score in self._rolling_m['scores']:
            col = self._cols[0] + '_' + str(each_score)
            self.ans_df.loc[row, col] = np.round(
                    end_bal_with_trans.get_value(each_score), self._dec)

    def _end_update_row(self, row):
        """
        Actualizar saldos finales
        Saldo Inicial + Desembolso - Amortizacion - Prepago - Castigo
        """
        self.ans_df.loc[row, "saldo_final_0"] = np.round((
            self.ans_df.loc[row, "saldo_inicial_0"] + self.ans_df.loc[
                row, "desembolso_0"] - self.ans_df.loc[row, "amortizacion_0"] -
            self.ans_df.loc[row, "prepago_0"] - self.ans_df.loc[
                row, "castigo_0"]), self._dec)
        self.ans_df.loc[row, "saldo_final_30"] = np.round((
            self.ans_df.loc[row, "saldo_inicial_30"] - self.ans_df.loc[
                row, "amortizacion_30"] - self.ans_df.loc[row, "prepago_30"] -
            self.ans_df.loc[row, "castigo_30"]), self._dec)
        self.ans_df.loc[row, "saldo_final_60"] = np.round((
            self.ans_df.loc[row, "saldo_inicial_60"] - self.ans_df.loc[
                row, "amortizacion_60"] - self.ans_df.loc[row, "prepago_60"] -
            self.ans_df.loc[row, "castigo_60"]), self._dec)
        self.ans_df.loc[row, "saldo_final_90"] = np.round((
            self.ans_df.loc[row, "saldo_inicial_90"] - self.ans_df.loc[
                row, "amortizacion_90"] - self.ans_df.loc[row, "prepago_90"] -
            self.ans_df.loc[row, "castigo_90"]), self._dec)
        self.ans_df.loc[row, "saldo_final_120"] = np.round((
            self.ans_df.loc[row, "saldo_inicial_120"] - self.ans_df.loc[
                row, "amortizacion_120"] - self.ans_df.loc[
                row, "prepago_120"] - self.ans_df.loc[row, "castigo_120"]),
                self._dec)
        self.ans_df.loc[row, "saldo_final_150"] = np.round((
            self.ans_df.loc[row, "saldo_inicial_150"] - self.ans_df.loc[
                row, "amortizacion_150"] - self.ans_df.loc[
                row, "prepago_150"] - self.ans_df.loc[row, "castigo_150"]),
                self._dec)
        self.ans_df.loc[row, "saldo_final_180"] = np.round((
            self.ans_df.loc[row, "saldo_inicial_180"] - self.ans_df.loc[
                row, "amortizacion_180"] - self.ans_df.loc[
                row, "prepago_180"] - self.ans_df.loc[row, "castigo_180"]),
                self._dec)
        self.ans_df.loc[row, "saldo_final_210"] = np.round((
            self.ans_df.loc[row, "saldo_inicial_210"] - self.ans_df.loc[
                row, "amortizacion_210"] - self.ans_df.loc[
                row, "prepago_210"] - self.ans_df.loc[row, "castigo_210"]),
                self._dec)

    def _prepay_update_row(self, row):
        """
        Computes prepayment by age and score
        Update output df
        """
        prepay_per_age = self._prepay[self.ans_df.index.get_loc(row)]
        a = self._prepay_score * prepay_per_age
        b = self._get_inicial_balance_row(row)
        c = a * b

        for each_score in self._rolling_m['scores']:
            col = self._cols[3] + '_' + str(each_score)
            self.ans_df.loc[row, col] = np.round(c.get_value(each_score),
                                                 self._dec)

    def _pay_update_row(self, row):
        """
        Computa el valor de amortizacion para un credito, dadas unas
        condiciones faciales

        """
        k = self.temp_struc[row] * self._notional
        i = self.tasas_nmv.get_value(row)
        per = row.to_period('M') - self._sdate.to_period('M')

        # output df
        ans = pd.Series(0.0, index = self._scores)

        for index, val in k.iteritems():
            # capital payment for each score
            if 0 < per <= self._nper:
                ppay = np.abs(np.ppmt(i, per, self._nper, val, 0))
                ppay = np.round(ppay * self._pay_calif[index], self._dec)
                ans.set_value(index, ppay)
            # despues del nper original cualquiera que se pone al dia va a
            # recaudo
            elif per > self._nper and index == 0:
                ans.set_value(index,
                              self.ans_df.loc[row, self._cols[0] + '_0'])



        # actualizar el dataframe de salida
        # debe verificar que el valor a amortizar existe despues de castigo
        # y prepago

        #for each_score in self._rolling_m['scores']:
        #    pay = self._cols[2] + '_' + str(each_score)
        #    i_b = self._cols[3] + '_' + str(each_score)
        #    prepay = self._cols[3] + '_' + str(each_score)
        #    w_off = self._cols[3] + '_' + str(each_score)

        self.ans_df.loc[row, "amortizacion_0"] = np.round(min((self.ans_df.loc[
                                                                   row,
                                                                   "saldo_inicial_0"] -
                                                               self.ans_df.loc[
                                                                   row,
                                                                   "prepago_0"] -
                                                               self.ans_df.loc[
                                                                   row,
                                                                   "castigo_0"]),
                                                              ans.get_value(
                                                                      0)),
                                                          self._dec)
        self.ans_df.loc[row, "amortizacion_30"] = np.round(min((
            self.ans_df.loc[row, "saldo_inicial_30"] - self.ans_df.loc[
                row, "prepago_30"] - self.ans_df.loc[row, "castigo_30"]),
                ans.get_value(30)), self._dec)
        self.ans_df.loc[row, "amortizacion_60"] = np.round(min((
            self.ans_df.loc[row, "saldo_inicial_60"] - self.ans_df.loc[
                row, "prepago_60"] - self.ans_df.loc[row, "castigo_60"]),
                ans.get_value(60)), self._dec)
        self.ans_df.loc[row, "amortizacion_90"] = np.round(min((
            self.ans_df.loc[row, "saldo_inicial_90"] - self.ans_df.loc[
                row, "prepago_90"] - self.ans_df.loc[row, "castigo_90"]),
                ans.get_value(90)), self._dec)
        self.ans_df.loc[row, "amortizacion_120"] = np.round(min((
            self.ans_df.loc[row, "saldo_inicial_120"] - self.ans_df.loc[
                row, "prepago_120"] - self.ans_df.loc[row, "castigo_120"]),
                ans.get_value(120)), self._dec)
        self.ans_df.loc[row, "amortizacion_150"] = np.round(min((
            self.ans_df.loc[row, "saldo_inicial_150"] - self.ans_df.loc[
                row, "prepago_150"] - self.ans_df.loc[row, "castigo_150"]),
                ans.get_value(150)), self._dec)
        self.ans_df.loc[row, "amortizacion_180"] = np.round(min((
            self.ans_df.loc[row, "saldo_inicial_180"] - self.ans_df.loc[
                row, "prepago_180"] - self.ans_df.loc[row, "castigo_180"]),
                ans.get_value(180)), self._dec)
        self.ans_df.loc[row, "amortizacion_210"] = np.round(min((
            self.ans_df.loc[row, "saldo_inicial_210"] - self.ans_df.loc[
                row, "prepago_210"] - self.ans_df.loc[row, "castigo_210"]),
                ans.get_value(210)), self._dec)

    def _write_off_update_row(self, row):
        """
        obtiene el % de castigo para cada calificacion
        aplica el factor de castigo a cada saldo inicial de acuerdo a su
        calificacion
        actualiza el dataframe de salida
        """
        a = self._write_off
        b = self._get_inicial_balance_row(row)
        c = a * b

        for each_score in self._rolling_m['scores']:
            col = self._cols[4] + '_' + str(each_score)
            self.ans_df.loc[row, col] = np.round(c.get_value(each_score),
                                                 self._dec)

    #############################################################
    # Private methods
    #############################################################

    def _temp_structure(self):
        """
        construye un diccionario con la estructura temporal de la cartera por
        calificacion aplicando la matriz de transicion para cada periodo
        """
        # crea un diccionario vacio con n keys desde la fecha de originacion
        dates_index = pd.date_range(self._sdate, periods = self._forecast,
                                    freq = 'M')
        ans_dict = dict.fromkeys(dates_index)

        for key in dates_index:
            m = self._matriz_de_transicion(key)
            if key == dates_index[0]:
                # mes cero, desembolso
                ans_dict[dates_index[0]] = pd.Series(
                        [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                        index = self._scores)
                # aplicar transicion y actualizar t+1
                ans = pd.Series(np.dot(np.transpose(m), ans_dict[key]),
                                index = self._scores)
                ans_dict[key + 1] = ans

            else:

                ans = pd.Series(np.dot(np.transpose(m), ans_dict[key]),
                                index = self._scores)
                ans_dict[key + 1] = ans

        # TODO: refactor para no repetir instrucciones
        return ans_dict

    def _tasas_full_nmv(self):
        """
        Computa la tasa full nmv para cada periodo basado en las
        caracteristicas
        faciales del name
        """
        # TODO: implementar diferentes indices
        # TODO: implementar reprecio
        if self._rate_type == "FIJA":
            return np.round(
                    self._spreads.apply(lambda x: (1 + x) ** (1 / 12) - 1), 6)
        elif self._rate_type == "DTF":
            pass
        elif self._rate_type == "IPC":
            pass
        elif self._rate_type == "IBR1":
            pass

    def _matriz_de_transicion(self, row):
        """
        locate the right transition matrix for the period.
        If not a correct matrix is found, look up for month = 1 else
        will give keyerror
        """

        if row.month in self._rolling_m.keys():
            return self._rolling_m[row.month]
        else:
            return self._rolling_m[1]

    def _apply_transition(self, row):
        """
        Apply a transition matrix to a vector of balances for delinquency,
        update end _balance of month 0 as
        beginning _balance month 1
        """

        sf_trans = pd.Series(
                np.dot(np.transpose(self._matriz_de_transicion(row)),
                       self._get_end_balance_row(row)), index = self._scores)

        if row + 1 <= self.ans_df.index[-1]:
            self._initial_update_row(row + 1, sf_trans)

    def _get_end_balance_row(self, row):
        """
        Obtiene una serie de saldos finales ordenados por calificacion

        """

        return np.round(pd.Series([self.ans_df.loc[row, "saldo_final_0"],
                                   self.ans_df.loc[row, "saldo_final_30"],
                                   self.ans_df.loc[row, "saldo_final_60"],
                                   self.ans_df.loc[row, "saldo_final_90"],
                                   self.ans_df.loc[row, "saldo_final_120"],
                                   self.ans_df.loc[row, "saldo_final_150"],
                                   self.ans_df.loc[row, "saldo_final_180"],
                                   self.ans_df.loc[row, "saldo_final_210"]],
                                  index = self._scores), self._dec)

    def _get_inicial_balance_row(self, row):
        """
        Obtiene una serie de saldos iniciales ordenados por calificacion
        """

        return np.round(pd.Series([self.ans_df.loc[row, "saldo_inicial_0"],
                                   self.ans_df.loc[row, "saldo_inicial_30"],
                                   self.ans_df.loc[row, "saldo_inicial_60"],
                                   self.ans_df.loc[row, "saldo_inicial_90"],
                                   self.ans_df.loc[row, "saldo_inicial_120"],
                                   self.ans_df.loc[row, "saldo_inicial_150"],
                                   self.ans_df.loc[row, "saldo_inicial_180"],
                                   self.ans_df.loc[row, "saldo_inicial_210"]],
                                  index = self._scores), self._dec)

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

    def get_balance(self, por_calif = False):
        """
        Construye el balance de la cosecha y lo exporta a un df
        se puede elegir entre vista por calificacion o vista agregada
        """
        if por_calif:
            return self.ans_df
        else:
            ans = pd.DataFrame(columns = (
                'saldo_inicial', 'desembolso', 'amortizacion', 'prepago',
                'castigo', 'saldo_final'), index = self.ans_df.index)
            for col in ans:
                ans[col] = self.get_serie(serie_name = col, por_calif = False)
            return ans

    def get_serie(self, serie_name = "saldo_final", por_calif = False):

        serie_name = serie_name.lower()
        if serie_name == "desembolso":
            ans = self.ans_df["desembolso_0"]
            por_calif = True
        else:
            ans = self.ans_df[
                [serie_name + "_" + str(0), serie_name + "_" + str(30),
                 serie_name + "_" + str(60), serie_name + "_" + str(90),
                 serie_name + "_" + str(120), serie_name + "_" + str(150),
                 serie_name + "_" + str(180), serie_name + "_" + str(210)]]

        if por_calif:
            return ans
        else:
            return ans.sum(axis = 1)

    def get_index(self):
        """
        Retorna el indice de fechas de la cosecha
        """
        return self.ans_df.index


if __name__ == '__main__':
    x1 = Cosecha_Credito(settings_cosecha())
    print("Linea de negocio: ", x1.name())
    print("Fecha de Originacion: ", x1.sdate())
    print("Plazo de Originacion: ", x1.nper())
    print("Tasas: ", x1.rate_type())
    print_tabulate(x1.get_balance(por_calif = True))
