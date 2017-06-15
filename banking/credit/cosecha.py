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
        self._rounding = 2
        self._max_forecast = settings['max_forecast']

        self._producto = settings['producto']
        self._plazo = settings['plazo']
        self._fecha_originacion = settings['fecha_originacion']
        self._desembolso = np.round(settings['desembolso'], self._rounding)

        self._alturas_mora = settings['alturas_mora']
        self._frecuencia_reprecio = settings['frecuencia_reprecio']

        self._tipo_tasa = settings['tipo_tasa']
        self._vector_tasas_indice = np.round(settings['vector_tasas_indice'],
                                             6)
        self._spread_originacion = np.round(settings['spread_originacion'], 6)

        self._vector_prepago = settings['vector_prepago']
        self._percent_prepago_por_calificacion = settings[
            'percent_prepago_por_calificacion']

        self._matrices_transcicion = settings['matrices_transicion']
        self._percent_amortizacion_por_calificacion = settings[
            'percent_recaudo_por_calificacion']
        self._percent_castigo_por_calificacion = settings[
            'percent_castigo_por_calificacion']

        # crear estructuras necesarias para operacion
        self.ans_df = self._df_structure()
        self.estructura_temporal = self._estructura_temporal_cartera()
        self.tasas_nmv = self._tasas_full_nmv()

        # llamado a la funcion principal que construye el balance de la cosecha
        # el objeto se crea al inicializar la clase
        self._constructor_de_balance()

    def _constructor_de_balance(self):
        """
        Construct a dataframe with projections of balances and cash flows for
        a loan portfolio in an homogeneous loan pool, where the loans share
        the same origination period.

        No amplia el tamaño del df

        :return: dataframe
        """

        # iterar cada fila
        for row, _col in self.ans_df.iterrows():

            # hacer desembolso en t+0
            if row == self.fecha_originacion():
                self.ans_df.loc[
                    self._fecha_originacion, 'desembolso_0'] = self._desembolso
            self._prepago_por_calificacion(row)
            #self._castigo_por_calificacion(row)
            #self._amortizacion_por_calificacion(row)
            #self._actualizar_saldo_final(row)
            #self._aplicar_transicion(row)

        return self.ans_df

    def _df_structure(self):
        """
        Crea la estructura del dataframe de salida
        :return pandas dataframe
        """

        col_names = ['saldo_inicial', 'desembolso', 'amortizacion', 'prepago',
                     'castigo', 'saldo_final']
        scores = self._matrices_transcicion['scores']

        cols = [each_col + "_" + str(each_score) for each_col in col_names for
                each_score in scores]
        dates_index = pd.date_range(self._fecha_originacion,
                                    periods = self._max_forecast,
                                    freq = 'M')

        return pd.DataFrame(0.0, index = dates_index, columns = cols)

    def _actualizar_saldo_final(self, row):
        """
        Actualizar saldos finales
        Saldo Inicial + Desembolso - Amortizacion - Prepago - Castigo
        """
        self.ans_df.loc[row, "saldo_final_0"] = np.round((
        self.ans_df.loc[row, "saldo_inicial_0"] + self.ans_df.loc[
            row, "desembolso_0"] - self.ans_df.loc[row, "amortizacion_0"] -
        self.ans_df.loc[row, "prepago_0"] - self.ans_df.loc[row, "castigo_0"]),
                self._rounding)
        self.ans_df.loc[row, "saldo_final_30"] = np.round((
        self.ans_df.loc[row, "saldo_inicial_30"] - self.ans_df.loc[
            row, "amortizacion_30"] - self.ans_df.loc[row, "prepago_30"] -
        self.ans_df.loc[row, "castigo_30"]), self._rounding)
        self.ans_df.loc[row, "saldo_final_60"] = np.round((
        self.ans_df.loc[row, "saldo_inicial_60"] - self.ans_df.loc[
            row, "amortizacion_60"] - self.ans_df.loc[row, "prepago_60"] -
        self.ans_df.loc[row, "castigo_60"]), self._rounding)
        self.ans_df.loc[row, "saldo_final_90"] = np.round((
        self.ans_df.loc[row, "saldo_inicial_90"] - self.ans_df.loc[
            row, "amortizacion_90"] - self.ans_df.loc[row, "prepago_90"] -
        self.ans_df.loc[row, "castigo_90"]), self._rounding)
        self.ans_df.loc[row, "saldo_final_120"] = np.round((
        self.ans_df.loc[row, "saldo_inicial_120"] - self.ans_df.loc[
            row, "amortizacion_120"] - self.ans_df.loc[row, "prepago_120"] -
        self.ans_df.loc[row, "castigo_120"]), self._rounding)
        self.ans_df.loc[row, "saldo_final_150"] = np.round((
        self.ans_df.loc[row, "saldo_inicial_150"] - self.ans_df.loc[
            row, "amortizacion_150"] - self.ans_df.loc[row, "prepago_150"] -
        self.ans_df.loc[row, "castigo_150"]), self._rounding)
        self.ans_df.loc[row, "saldo_final_180"] = np.round((
        self.ans_df.loc[row, "saldo_inicial_180"] - self.ans_df.loc[
            row, "amortizacion_180"] - self.ans_df.loc[row, "prepago_180"] -
        self.ans_df.loc[row, "castigo_180"]), self._rounding)
        self.ans_df.loc[row, "saldo_final_210"] = np.round((
        self.ans_df.loc[row, "saldo_inicial_210"] - self.ans_df.loc[
            row, "amortizacion_210"] - self.ans_df.loc[row, "prepago_210"] -
        self.ans_df.loc[row, "castigo_210"]), self._rounding)

    def _prepago_por_calificacion(self, row):
        """
        Obtiene el valor % de prepago que aplica para una edad y calificacion
        aplica el factor de prepago a cada saldo inicial de acuerdo a su
        calificacion
        actualiza el dataframe de salida

        """
        prepago_por_edad = self._vector_prepago[self.ans_df.index.get_loc(row)]
        print(prepago_por_edad)
        a = self._percent_prepago_por_calificacion * prepago_por_edad
        b = self._saldo_inicial_by_row(row)
        c = a * b

        # actualizar el dataframe de salida
        self.ans_df.loc[row, "prepago_0"] = np.round(c.get_value(0), self._rounding)
        self.ans_df.loc[row, "prepago_30"] = np.round(c.get_value(30),self._rounding)
        self.ans_df.loc[row, "prepago_60"] = np.round(c.get_value(60),
                                                     self._rounding)
        self.ans_df.loc[row, "prepago_90"] = np.round(c.get_value(90),
                                                     self._rounding)
        self.ans_df.loc[row, "prepago_120"] = np.round(c.get_value(120),
                                                      self._rounding)
        self.ans_df.loc[row, "prepago_150"] = np.round(c.get_value(150),
                                                      self._rounding)
        self.ans_df.loc[row, "prepago_180"] = np.round(c.get_value(180),
                                                      self._rounding)
        self.ans_df.loc[row, "prepago_210"] = np.round(c.get_value(210),
                                                      self._rounding)

    def _castigo_por_calificacion(self, row):
        """
        obtiene el % de castigo para cada calificacion
        aplica el factor de castigo a cada saldo inicial de acuerdo a su
        calificacion
        actualiza el dataframe de salida
        """
        a = self._percent_castigo_por_calificacion
        b = self._saldo_inicial_by_row(row)
        c = a * b

        # actualizar el dataframe de salida
        self.ans_df.loc[row, "castigo_0"] = np.round(c.get_value(0),
                                                    self._rounding)
        self.ans_df.loc[row, "castigo_30"] = np.round(c.get_value(30),
                                                     self._rounding)
        self.ans_df.loc[row, "castigo_60"] = np.round(c.get_value(60),
                                                     self._rounding)
        self.ans_df.loc[row, "castigo_90"] = np.round(c.get_value(90),
                                                     self._rounding)
        self.ans_df.loc[row, "castigo_120"] = np.round(c.get_value(120),
                                                      self._rounding)
        self.ans_df.loc[row, "castigo_150"] = np.round(c.get_value(150),
                                                      self._rounding)
        self.ans_df.loc[row, "castigo_180"] = np.round(c.get_value(180),
                                                      self._rounding)
        self.ans_df.loc[row, "castigo_210"] = np.round(c.get_value(210),
                                                      self._rounding)

    def _estructura_temporal_cartera(self):
        """
        construye un diccionario con la estructura temporal de la cartera por
        calificacion aplicando la matriz de transicion para cada periodo
        """
        # crea un diccionario vacio con n keys desde la fecha de originacion
        dates_index = pd.date_range(self.fecha_originacion(),
                                    periods=self._max_forecast, freq='M')
        ans_dict = dict.fromkeys(dates_index)

        for key in dates_index:
            m = self._matriz_de_transicion(key)
            if key == dates_index[0]:
                # mes cero, desembolso
                ans_dict[dates_index[0]] = pd.Series(
                        [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                        index=self._alturas_mora)
                # aplicar transicion y actualizar t+1
                ans = pd.Series(np.dot(np.transpose(m), ans_dict[key]),
                                index=self._alturas_mora)
                ans_dict[key + 1] = ans

            else:

                ans = pd.Series(np.dot(np.transpose(m), ans_dict[key]),
                                index=self._alturas_mora)
                ans_dict[key + 1] = ans

        # TODO: refactor para no repetir instrucciones
        return ans_dict

    def _tasas_full_nmv(self):
        """
        Computa la tasa full nmv para cada periodo basado en las
        caracteristicas
        faciales del producto
        """
        # TODO: implementar diferentes indices
        # TODO: implementar reprecio
        if self._tipo_tasa == "FIJA":
            return np.round(self._spread_originacion.apply(
                lambda x: (1 + x) ** (1 / 12) - 1), 6)
        elif self._tipo_tasa == "DTF":
            pass
        elif self._tipo_tasa == "IPC":
            pass
        elif self._tipo_tasa == "IBR1":
            pass

    def _amortizacion_por_calificacion(self, row):
        """
        Computa el valor de amortizacion para un credito, dadas unas
        condiciones faciales

        """
        k = self.estructura_temporal[row] * self._desembolso
        i = self.tasas_nmv.get_value(row)
        nper = self._plazo
        per = row.to_period('M') - self._fecha_originacion.to_period('M')

        # df de salida
        ans = pd.Series(0.0, index=self._alturas_mora)

        for index, val in k.iteritems():
            # calcular el pago de principal para cada calificacion
            if per > 0 and per <= nper:
                ppay = np.abs(np.ppmt(i, per, nper, val, 0))
                ppay = np.round(
                        ppay * self._percent_amortizacion_por_calificacion[
                            index], self._rounding)
                ans.set_value(index, ppay)
            # despues del plazo original cualquiera que se pone al dia va a
            # recaudo
            elif per > nper and index == 0:
                ans.set_value(index, self.ans_df.loc[row, "saldo_inicial_0"])

        # actualizar el dataframe de salida
        # debe verificar que el valor a amortizar existe despues de castigo
        # y prepago
        self.ans_df.loc[row, "amortizacion_0"] = np.round(min((self.ans_df.loc[
                                                                  row,
                                                                  "saldo_inicial_0"] -
                                                              self.ans_df.loc[
                                                                  row,
                                                                  "prepago_0"] -
                                                              self.ans_df.loc[
                                                                  row,
                                                                  "castigo_0"]),
                                                             ans.get_value(0)),
                self._rounding)
        self.ans_df.loc[row, "amortizacion_30"] = np.round(min((
            self.ans_df.loc[
                                                                   row,
                                                                   "saldo_inicial_30"] -
                                                               self.ans_df.loc[
                                                                   row,
                                                                   "prepago_30"] -
                                                               self.ans_df.loc[
                                                                   row,
                                                                   "castigo_30"]),
                                                              ans.get_value(
                                                                  30)),
                self._rounding)
        self.ans_df.loc[row, "amortizacion_60"] = np.round(min((
            self.ans_df.loc[
                                                                   row,
                                                                   "saldo_inicial_60"] -
                                                               self.ans_df.loc[
                                                                   row,
                                                                   "prepago_60"] -
                                                               self.ans_df.loc[
                                                                   row,
                                                                   "castigo_60"]),
                                                              ans.get_value(
                                                                  60)),
                self._rounding)
        self.ans_df.loc[row, "amortizacion_90"] = np.round(min((
            self.ans_df.loc[
                                                                   row,
                                                                   "saldo_inicial_90"] -
                                                               self.ans_df.loc[
                                                                   row,
                                                                   "prepago_90"] -
                                                               self.ans_df.loc[
                                                                   row,
                                                                   "castigo_90"]),
                                                              ans.get_value(
                                                                  90)),
                self._rounding)
        self.ans_df.loc[row, "amortizacion_120"] = np.round(min((
                                                               self.ans_df.loc[
                                                                   row,
                                                                   "saldo_inicial_120"] -
                                                               self.ans_df.loc[
                                                                   row,
                                                                   "prepago_120"] -
                                                               self.ans_df.loc[
                                                                   row,
                                                                   "castigo_120"]),
                                                               ans.get_value(
                                                                   120)),
                self._rounding)
        self.ans_df.loc[row, "amortizacion_150"] = np.round(min((
                                                               self.ans_df.loc[
                                                                   row,
                                                                   "saldo_inicial_150"] -
                                                               self.ans_df.loc[
                                                                   row,
                                                                   "prepago_150"] -
                                                               self.ans_df.loc[
                                                                   row,
                                                                   "castigo_150"]),
                                                               ans.get_value(
                                                                   150)),
                self._rounding)
        self.ans_df.loc[row, "amortizacion_180"] = np.round(min((
                                                               self.ans_df.loc[
                                                                   row,
                                                                   "saldo_inicial_180"] -
                                                               self.ans_df.loc[
                                                                   row,
                                                                   "prepago_180"] -
                                                               self.ans_df.loc[
                                                                   row,
                                                                   "castigo_180"]),
                                                               ans.get_value(
                                                                   180)),
                self._rounding)
        self.ans_df.loc[row, "amortizacion_210"] = np.round(min((
                                                               self.ans_df.loc[
                                                                   row,
                                                                   "saldo_inicial_210"] -
                                                               self.ans_df.loc[
                                                                   row,
                                                                   "prepago_210"] -
                                                               self.ans_df.loc[
                                                                   row,
                                                                   "castigo_210"]),
                                                               ans.get_value(
                                                                   210)),
                self._rounding)

    def _matriz_de_transicion(self, row):
        """
        locate the right transition matrix for the period.
        If not a correct matrix is found, look up for month = 1 else
        will give keyerror
        """

        if row.month in self._matrices_transcicion.keys():
            return self._matrices_transcicion[row.month]
        else:
            return self._matrices_transcicion[1]

    def _aplicar_transicion(self, row):
        """
        Apply a transition matrix to a vector of balances for delinquency,
        update end _constructor_de_balance of month 0 as
        beginning _constructor_de_balance month 1
        """

        sf_trans = pd.Series(
            np.dot(np.transpose(self._matriz_de_transicion(row)),
                   self._saldo_final_by_row(row)), index=self._alturas_mora)

        if row + 1 <= self.ans_df.index[-1]:
            self._actualizar_saldo_inicial(row + 1, sf_trans)

    def _actualizar_saldo_inicial(self, row, vector_final_con_transicion):
        """
        Actualiza el saldo inicial de un periodo como el saldo final del
        periodo anterior aplicada la matriz de transicion por calificacion
        """

        self.ans_df.loc[row, "saldo_inicia_l0"] = np.round(
                vector_final_con_transicion.get_value(0), self._rounding)
        self.ans_df.loc[row, "saldo_inicial_30"] = np.round(
                vector_final_con_transicion.get_value(30), self._rounding)
        self.ans_df.loc[row, "saldo_inicial_60"] = np.round(
                vector_final_con_transicion.get_value(60), self._rounding)
        self.ans_df.loc[row, "saldo_inicia_l90"] = np.round(
                vector_final_con_transicion.get_value(90), self._rounding)
        self.ans_df.loc[row, "saldo_inicial_120"] = np.round(
                vector_final_con_transicion.get_value(120), self._rounding)
        self.ans_df.loc[row, "saldo_inicial_150"] = np.round(
                vector_final_con_transicion.get_value(150), self._rounding)
        self.ans_df.loc[row, "saldo_inicial_180"] = np.round(
                vector_final_con_transicion.get_value(180), self._rounding)
        self.ans_df.loc[row, "saldo_inicial_210"] = np.round(
                vector_final_con_transicion.get_value(210), self._rounding)

    def _saldo_final_by_row(self, row):
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
                                  index=self._alturas_mora), self._rounding)

    def _saldo_inicial_by_row(self, row):
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
                                  index=self._alturas_mora), self._rounding)

    def producto(self):
        """
        :return: str linea de negocio
        """
        return self._producto

    def plazo(self):
        """
        :return: int
        """
        return self._plazo

    def fecha_originacion(self):
        """
        :return: date
        """
        return self._fecha_originacion

    def tipo_tasa(self):
        """
        :return: list [tipo tasa, valor]
        """
        return [self._tipo_tasa, self._spread_originacion[0]]

    def get_balance(self, por_calif=False):
        """
        Construye el balance de la cosecha y lo exporta a un df
        se puede elegir entre vista por calificacion o vista agregada
        """
        if por_calif:
            return self.ans_df

        else:
            ans = pd.DataFrame(columns=(
            'saldo_inicial', 'desembolso', 'amortizacion', 'prepago',
            'castigo', 'saldo_final'), index=self.ans_df.index)
            for col in ans:
                ans[col] = self.get_serie(serie_name=col, por_calif=False)
            return ans

    def get_serie(self, serie_name="saldo_final", por_calif=False):

        serie_name = serie_name.lower()
        if serie_name == "desembolso":
            ans = self.ans_df["desembolso_0"]
            por_calif = True
        else:
            ans = self.ans_df[[serie_name + "_" + str(0), serie_name + "_" + str(30),
                               serie_name + "_" + str(60), serie_name + "_" + str(90),
                               serie_name + "_" + str(120), serie_name + "_" + str(150),
                               serie_name + "_" + str(180), serie_name + "_" + str(210)]]

        if por_calif:
            return ans
        else:
            return ans.sum(axis=1)

    def get_index(self):
        """
        Retorna el indice de fechas de la cosecha
        """
        return self.ans_df.index






if __name__ == '__main__':
    x1 = Cosecha_Credito(settings_cosecha())
    print("Linea de negocio: ", x1.producto())
    print("Fecha de Originacion: ", x1.fecha_originacion())
    print("Plazo de Originacion: ", x1.plazo())
    print("Tasas: ", x1.tipo_tasa())
    print_tabulate(x1.get_balance(por_calif = True))
