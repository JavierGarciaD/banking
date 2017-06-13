from sphinx.util.inspect import inspect

from develop_testing.pruebas1 import settings_cosecha
import numpy as np
import pandas as pd


class Cosecha_Credito:
    def __init__(self, settings):
        """
        Construct an object with information for a loan portfolio on
        an homogeneous loan pool, where the loans share the same origination period.
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
        self._vector_tasas_indice = np.round(settings['vector_tasas_indice'], 6)
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
                    self._fecha_originacion, 'desembolso0'] = self._desembolso

            self._prepago_por_calificacion(row)
            self._castigo_por_calificacion(row)
            self._amortizacion_por_calificacion(row)
            self._actualizar_saldo_final(row)
            self._aplicar_transicion(row)

        return self.ans_df

    def _df_structure(self):
        """
        Crea la estructura del dataframe de salida
        :return pandas dataframe
        """

        dates_index = pd.date_range(self.fecha_originacion(),
                                    periods=self._max_forecast,
                                    freq='M')

        return pd.DataFrame(0.0,
                            index=dates_index,
                            columns=('saldo_inicial0', 'saldo_inicial30',
                                     'saldo_inicial60', 'saldo_inicial90',
                                     'saldo_inicial120',
                                     'saldo_inicial150', 'saldo_inicial180',
                                     'saldo_inicial210',
                                     'desembolso0',
                                     'amortizacion0', 'amortizacion30', 'amortizacion60',
                                     'amortizacion90',
                                     'amortizacion120', 'amortizacion150',
                                     'amortizacion180', 'amortizacion210',
                                     'prepago0', 'prepago30', 'prepago60', 'prepago90',
                                     'prepago120', 'prepago150', 'prepago180',
                                     'prepago210',
                                     'castigo0', 'castigo30', 'castigo60', 'castigo90',
                                     'castigo120', 'castigo150', 'castigo180',
                                     'castigo210',
                                     'saldo_final0', 'saldo_final30', 'saldo_final60',
                                     'saldo_final90',
                                     'saldo_final120', 'saldo_final150',
                                     'saldo_final180',
                                     'saldo_final210'))

    def _actualizar_saldo_final(self, row):
        """
        Actualizar saldos finales
        Saldo Inicial + Desembolso - Amortizacion - Prepago - Castigo
        """
        self.ans_df.loc[row, "saldo_final0"] = np.round(
                (self.ans_df.loc[row, "saldo_inicial0"]
                 + self.ans_df.loc[row, "desembolso0"]
                 - self.ans_df.loc[row, "amortizacion0"]
                 - self.ans_df.loc[row, "prepago0"]
                 - self.ans_df.loc[row, "castigo0"]),
                self._rounding)
        self.ans_df.loc[row, "saldo_final30"] = np.round(
                (self.ans_df.loc[row, "saldo_inicial30"]
                 - self.ans_df.loc[row, "amortizacion30"]
                 - self.ans_df.loc[row, "prepago30"]
                 - self.ans_df.loc[row, "castigo30"]),
                self._rounding)
        self.ans_df.loc[row, "saldo_final60"] = np.round(
                (self.ans_df.loc[row, "saldo_inicial60"]
                 - self.ans_df.loc[row, "amortizacion60"]
                 - self.ans_df.loc[row, "prepago60"]
                 - self.ans_df.loc[row, "castigo60"]),
                self._rounding)
        self.ans_df.loc[row, "saldo_final90"] = np.round(
                (self.ans_df.loc[row, "saldo_inicial90"]
                 - self.ans_df.loc[row, "amortizacion90"]
                 - self.ans_df.loc[row, "prepago90"]
                 - self.ans_df.loc[row, "castigo90"]),
                self._rounding)
        self.ans_df.loc[row, "saldo_final120"] = np.round(
                (self.ans_df.loc[row, "saldo_inicial120"]
                 - self.ans_df.loc[row, "amortizacion120"]
                 - self.ans_df.loc[row, "prepago120"]
                 - self.ans_df.loc[row, "castigo120"]),
                self._rounding)
        self.ans_df.loc[row, "saldo_final150"] = np.round(
                (self.ans_df.loc[row, "saldo_inicial150"]
                 - self.ans_df.loc[row, "amortizacion150"]
                 - self.ans_df.loc[row, "prepago150"]
                 - self.ans_df.loc[row, "castigo150"]),
                self._rounding)
        self.ans_df.loc[row, "saldo_final180"] = np.round(
                (self.ans_df.loc[row, "saldo_inicial180"]
                 - self.ans_df.loc[row, "amortizacion180"]
                 - self.ans_df.loc[row, "prepago180"]
                 - self.ans_df.loc[row, "castigo180"]),
                self._rounding)
        self.ans_df.loc[row, "saldo_final210"] = np.round(
                (self.ans_df.loc[row, "saldo_inicial210"]
                 - self.ans_df.loc[row, "amortizacion210"]
                 - self.ans_df.loc[row, "prepago210"]
                 - self.ans_df.loc[row, "castigo210"]),
                self._rounding)

    def _prepago_por_calificacion(self, row):
        """
        Obtiene el valor % de prepago que aplica para una edad y calificacion
        aplica el factor de prepago a cada saldo inicial de acuerdo a su calificacion
        actualiza el dataframe de salida

        """
        prepago_por_edad = self._vector_prepago[self.ans_df.index.get_loc(row)]
        a = self._percent_prepago_por_calificacion * prepago_por_edad
        b = self._saldo_inicial_by_row(row)
        c = a * b

        # actualizar el dataframe de salida
        self.ans_df.loc[row, "prepago0"] = np.round(c.get_value(0), self._rounding)
        self.ans_df.loc[row, "prepago30"] = np.round(c.get_value(30), self._rounding)
        self.ans_df.loc[row, "prepago60"] = np.round(c.get_value(60), self._rounding)
        self.ans_df.loc[row, "prepago90"] = np.round(c.get_value(90), self._rounding)
        self.ans_df.loc[row, "prepago120"] = np.round(c.get_value(120), self._rounding)
        self.ans_df.loc[row, "prepago150"] = np.round(c.get_value(150), self._rounding)
        self.ans_df.loc[row, "prepago180"] = np.round(c.get_value(180), self._rounding)
        self.ans_df.loc[row, "prepago210"] = np.round(c.get_value(210), self._rounding)

    def _castigo_por_calificacion(self, row):
        """
        obtiene el % de castigo para cada calificacion
        aplica el factor de castigo a cada saldo inicial de acuerdo a su calificacion
        actualiza el dataframe de salida
        """
        a = self._percent_castigo_por_calificacion
        b = self._saldo_inicial_by_row(row)
        c = a * b

        # actualizar el dataframe de salida
        self.ans_df.loc[row, "castigo0"] = np.round(c.get_value(0), self._rounding)
        self.ans_df.loc[row, "castigo30"] = np.round(c.get_value(30), self._rounding)
        self.ans_df.loc[row, "castigo60"] = np.round(c.get_value(60), self._rounding)
        self.ans_df.loc[row, "castigo90"] = np.round(c.get_value(90), self._rounding)
        self.ans_df.loc[row, "castigo120"] = np.round(c.get_value(120), self._rounding)
        self.ans_df.loc[row, "castigo150"] = np.round(c.get_value(150), self._rounding)
        self.ans_df.loc[row, "castigo180"] = np.round(c.get_value(180), self._rounding)
        self.ans_df.loc[row, "castigo210"] = np.round(c.get_value(210), self._rounding)

    def _estructura_temporal_cartera(self):
        """
        construye un diccionario con la estructura temporal de la cartera por
        calificacion aplicando la matriz de transicion para cada periodo
        """
        # crea un diccionario vacio con n keys desde la fecha de originacion
        dates_index = pd.date_range(self.fecha_originacion(), periods=self._max_forecast,
                                    freq='M')
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
        Computa la tasa full nmv para cada periodo basado en las caracteristicas
        faciales del producto
        """
        # TODO: implementar diferentes indices
        # TODO: implementar reprecio
        if self._tipo_tasa == "FIJA":
            return np.round(
                self._spread_originacion.apply(lambda x: (1 + x) ** (1 / 12) - 1),
                6)
        elif self._tipo_tasa == "DTF":
            pass
        elif self._tipo_tasa == "IPC":
            pass
        elif self._tipo_tasa == "IBR1":
            pass

    def _amortizacion_por_calificacion(self, row):
        """
        Computa el valor de amortizacion para un credito, dadas unas condiciones faciales

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
                    ppay * self._percent_amortizacion_por_calificacion[index],
                    self._rounding)
                ans.set_value(index, ppay)
            # despues del plazo original cualquiera que se pone al dia va a recaudo
            elif per > nper and index == 0:
                ans.set_value(index, self.ans_df.loc[row, "saldo_inicial0"])

        # actualizar el dataframe de salida
        # debe verificar que el valor a amortizar existe despues de castigo y prepago
        self.ans_df.loc[row, "amortizacion0"] = np.round(
            min((self.ans_df.loc[row, "saldo_inicial0"]
                 - self.ans_df.loc[row, "prepago0"]
                 - self.ans_df.loc[row, "castigo0"]),
                ans.get_value(0)),
            self._rounding)
        self.ans_df.loc[row, "amortizacion30"] = np.round(
            min((self.ans_df.loc[row, "saldo_inicial30"]
                 - self.ans_df.loc[row, "prepago30"]
                 - self.ans_df.loc[row, "castigo30"]),
                ans.get_value(30)),
            self._rounding)
        self.ans_df.loc[row, "amortizacion60"] = np.round(
            min((self.ans_df.loc[row, "saldo_inicial60"]
                 - self.ans_df.loc[row, "prepago60"]
                 - self.ans_df.loc[row, "castigo60"]),
                ans.get_value(60)),
            self._rounding)
        self.ans_df.loc[row, "amortizacion90"] = np.round(
            min((self.ans_df.loc[row, "saldo_inicial90"]
                 - self.ans_df.loc[row, "prepago90"]
                 - self.ans_df.loc[row, "castigo90"]),
                ans.get_value(90)),
            self._rounding)
        self.ans_df.loc[row, "amortizacion120"] = np.round(
            min((self.ans_df.loc[row, "saldo_inicial120"]
                 - self.ans_df.loc[row, "prepago120"]
                 - self.ans_df.loc[row, "castigo120"]),
                ans.get_value(120)),
            self._rounding)
        self.ans_df.loc[row, "amortizacion150"] = np.round(
            min((self.ans_df.loc[row, "saldo_inicial150"]
                 - self.ans_df.loc[row, "prepago150"]
                 - self.ans_df.loc[row, "castigo150"]),
                ans.get_value(150)),
            self._rounding)
        self.ans_df.loc[row, "amortizacion180"] = np.round(
            min((self.ans_df.loc[row, "saldo_inicial180"]
                 - self.ans_df.loc[row, "prepago180"]
                 - self.ans_df.loc[row, "castigo180"]),
                ans.get_value(180)),
            self._rounding)
        self.ans_df.loc[row, "amortizacion210"] = np.round(
            min((self.ans_df.loc[row, "saldo_inicial210"]
                 - self.ans_df.loc[row, "prepago210"]
                 - self.ans_df.loc[row, "castigo210"]),
                ans.get_value(210)),
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

        sf_trans = pd.Series(np.dot(np.transpose(self._matriz_de_transicion(row)),
                                    self._saldo_final_by_row(row)),
                             index=self._alturas_mora)

        if row + 1 <= self.ans_df.index[-1]:
            self._actualizar_saldo_inicial(row + 1, sf_trans)

    def _actualizar_saldo_inicial(self, row, vector_final_con_transicion):
        """
        Actualiza el saldo inicial de un periodo como el saldo final del
        periodo anterior aplicada la matriz de transicion por calificacion
        """

        self.ans_df.loc[row, "saldo_inicial0"] = np.round(
            vector_final_con_transicion.get_value(0),
            self._rounding)
        self.ans_df.loc[row, "saldo_inicial30"] = np.round(
            vector_final_con_transicion.get_value(30),
            self._rounding)
        self.ans_df.loc[row, "saldo_inicial60"] = np.round(
            vector_final_con_transicion.get_value(60),
            self._rounding)
        self.ans_df.loc[row, "saldo_inicial90"] = np.round(
            vector_final_con_transicion.get_value(90),
            self._rounding)
        self.ans_df.loc[row, "saldo_inicial120"] = np.round(
            vector_final_con_transicion.get_value(120),
            self._rounding)
        self.ans_df.loc[row, "saldo_inicial150"] = np.round(
            vector_final_con_transicion.get_value(150),
            self._rounding)
        self.ans_df.loc[row, "saldo_inicial180"] = np.round(
            vector_final_con_transicion.get_value(180),
            self._rounding)
        self.ans_df.loc[row, "saldo_inicial210"] = np.round(
            vector_final_con_transicion.get_value(210),
            self._rounding)

    def _saldo_final_by_row(self, row):
        """
        Obtiene una serie de saldos finales ordenados por calificacion

        """

        return np.round(pd.Series([self.ans_df.loc[row, "saldo_final0"],
                                   self.ans_df.loc[row, "saldo_final30"],
                                   self.ans_df.loc[row, "saldo_final60"],
                                   self.ans_df.loc[row, "saldo_final90"],
                                   self.ans_df.loc[row, "saldo_final120"],
                                   self.ans_df.loc[row, "saldo_final150"],
                                   self.ans_df.loc[row, "saldo_final180"],
                                   self.ans_df.loc[row, "saldo_final210"]],
                                  index=self._alturas_mora),
                        self._rounding)

    def _saldo_inicial_by_row(self, row):
        """
        Obtiene una serie de saldos iniciales ordenados por calificacion
        """

        return np.round(pd.Series([self.ans_df.loc[row, "saldo_inicial0"],
                                   self.ans_df.loc[row, "saldo_inicial30"],
                                   self.ans_df.loc[row, "saldo_inicial60"],
                                   self.ans_df.loc[row, "saldo_inicial90"],
                                   self.ans_df.loc[row, "saldo_inicial120"],
                                   self.ans_df.loc[row, "saldo_inicial150"],
                                   self.ans_df.loc[row, "saldo_inicial180"],
                                   self.ans_df.loc[row, "saldo_inicial210"]],
                                  index=self._alturas_mora),
                        self._rounding)

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
            ans = pd.DataFrame(columns=('saldo_inicial', 'desembolso',
                                        'amortizacion', 'prepago', 'castigo',
                                        'saldo_final'),
                               index=self.ans_df.index)
            for col in ans:
                ans[col] = self.get_serie(serie_name=col, por_calif=False)
            return ans

    def get_serie(self, serie_name="saldo_final", por_calif=False):

        serie_name = serie_name.lower()
        if serie_name == "desembolso":
            ans = self.ans_df["desembolso0"]
            por_calif = True
        else:
            ans = self.ans_df[[serie_name + str(0),
                               serie_name + str(30),
                               serie_name + str(60),
                               serie_name + str(90),
                               serie_name + str(120),
                               serie_name + str(150),
                               serie_name + str(180),
                               serie_name + str(210)]]

        if por_calif == True:
            return ans
        else:
            return ans.sum(axis=1)

    def get_index(self):
        """
        Retorna el indice de fechas de la cosecha
        """
        return self.ans_df.index


def estructura_temporal_cartera(m_dict, start_date, nper):
    """
    :summary: construye un diccionario con la estructura temporal
    de la cartera por calificacion, aplicando la matriz de
    transicion para cada periodo

    :param m_dict: dictionary con 1 o 12 matrices de transicion
    :param start_date: fecha de inicio
    :param nper: numero de periodos a proyectar

    :type m_dict: dict
    :type nper: int

    :return:
    :rtype: dict
    """

    # crea un diccionario vacio con n keys desde la fecha de originacion
    dates_index = pd.date_range(start_date, periods=nper, freq='M')
    ans_dict = dict.fromkeys(dates_index)

    for key in m_dict:
        m = m_dict(key)
        scores = m_dict(key).keys()
        if key == dates_index[0]:
            # mes cero, desembolso
            ans_dict[dates_index[0]] = pd.Series(
                    [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    index=scores)
            # aplicar transicion y actualizar t+1
            ans = pd.Series(np.dot(np.transpose(m), ans_dict[key]),
                            index=scores)
            ans_dict[key + 1] = ans

        else:
            ans = pd.Series(np.dot(np.transpose(m), ans_dict[key]),
                            index=scores)
            ans_dict[key + 1] = ans

        return ans_dict


if __name__ == '__main__':
    x1 = Cosecha_Credito(settings_cosecha())
    print("Linea de negocio: ", x1.producto())
    print("Fecha de Originacion: ", x1.fecha_originacion())
    print("Plazo de Originacion: ", x1.plazo())
    print("Tasas: ", x1.tipo_tasa())
    print(x1.get_serie(serie_name="saldo_final", por_calif=False))
