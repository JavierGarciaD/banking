
# -*- coding: utf-8 -*-
import timeit
import numpy as np
import pandas as pd
from decimal import Decimal, getcontext, ROUND_HALF_DOWN
from develop_testing.pruebas1 import *
from pprint import pprint

class Cosecha_Credito:
    #===========================================================================
    # Construct an object with information for a loan portfolio on
    # an homogeneous loan pool, where the loans share the same origination period.
    #===========================================================================

    def __init__(self, settings):
        """

        """
        self._producto = settings['producto']
        self._tipo_tasa = settings['tipo_tasa']
        self._alturas_mora = settings['alturas_mora']
        self._frecuencia_reprecio = settings['frecuencia_reprecio']
        self._plazo = settings['plazo']
        self._fecha_originacion = settings['fecha_originacion']
        self._desembolso = settings['desembolso']

        self._vector_tasas_indice = settings['vector_tasas_indice']
        self._spread_originacion = settings['spread_originacion']

        self._vector_prepago = settings['vector_prepago']
        self._percent_prepago_por_calificacion = settings['percent_prepago_por_calificacion']

        self._matrices_transcicion = settings['matrices_transicion']
        self._percent_amortizacion_por_calificacion = settings['percent_recaudo_por_calificacion']
        self._percent_castigo_por_calificacion = settings['percent_castigo_por_calificacion']
        self._percent_provision_por_calificacion = settings['percent_provision_por_calificacion']

        self._max_forecast = settings['max_forecast']

        # crear estructuras necesarias para operacion
        self.ans_df = self._df_structure()
        self.estructura_temporal = self._estructura_temporal_cartera()
        self.tasas_nmv = self._tasas_full_nmv()


    def producto(self):
        """
        :return: str
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


    def constructor_de_balance(self):
        """
        Construct a dataframe with projections of balances and cash flows for
        a loan portfolio in an homogeneous loan pool, where the loans share
        the same origination period.
        :return: dataframe
        """

        

        # iterar cada fila
        for row, _col in self.ans_df.iterrows():

            # hacer desembolso en t+0
            if row == self.fecha_originacion():
                self.ans_df.loc[self._fecha_originacion, 'desembolso0'] = self._desembolso


            self._prepago_por_calificacion(row)

            self._castigo_por_calificacion(row)

            self._amortizacion_por_calificacion(row)

            self._actualizar_saldo_final(row)

            self._aplicar_transicion(row)

            # ampliar el dataframe si aun hay saldos
            #if self.ans_df.shape[0] > rango:
            #    rango = self.ans_df.shape[0]
            #    i = i - 1

        return self.ans_df


    def _df_structure(self):
        """
        Crea la estructura del dataframe de salida
        :return pandas dataframe
        """

        dates_index = pd.date_range(self.fecha_originacion(), periods = self._max_forecast , freq = 'M')

        return pd.DataFrame(0.0,
                            index = dates_index,
                            columns = ('saldo_inicial0', 'saldo_inicial30', 'saldo_inicial60',
                            'saldo_inicial90', 'saldo_inicial120', 'saldo_inicial150',
                            'saldo_inicial180', 'saldo_inicial210',
                            'desembolso0',
                            'amortizacion0', 'amortizacion30', 'amortizacion60', 'amortizacion90',
                            'amortizacion120', 'amortizacion150', 'amortizacion180', 'amortizacion210',
                            'prepago0', 'prepago30', 'prepago60', 'prepago90',
                            'prepago120', 'prepago150', 'prepago180', 'prepago210',
                            'castigo0', 'castigo30', 'castigo60', 'castigo90',
                            'castigo120', 'castigo150', 'castigo180', 'castigo210',
                            'saldo_final0', 'saldo_final30', 'saldo_final60', 'saldo_final90',
                            'saldo_final120', 'saldo_final150', 'saldo_final180',
                            'saldo_final210'))


    def _actualizar_saldo_final(self, row):
        """
        Actualizar saldos finales
        Saldo Inicial + Desembolso - Amortizacion - Prepago - Castigo
        """
        self.ans_df.loc[row, "saldo_final0"] = (self.ans_df.loc[row, "saldo_inicial0"]
                                                + self.ans_df.loc[row, "desembolso0"]
                                                - self.ans_df.loc[row, "amortizacion0"]
                                                - self.ans_df.loc[row, "prepago0"]
                                                - self.ans_df.loc[row, "castigo0"])
        self.ans_df.loc[row, "saldo_final30"] = (self.ans_df.loc[row, "saldo_inicial30"]
                                                 - self.ans_df.loc[row, "amortizacion30"]
                                                 - self.ans_df.loc[row, "prepago30"]
                                                 - self.ans_df.loc[row, "castigo30"])
        self.ans_df.loc[row, "saldo_final60"] = (self.ans_df.loc[row, "saldo_inicial60"]
                                                 - self.ans_df.loc[row, "amortizacion60"]
                                                 - self.ans_df.loc[row, "prepago60"]
                                                 - self.ans_df.loc[row, "castigo60"])
        self.ans_df.loc[row, "saldo_final90"] = (self.ans_df.loc[row, "saldo_inicial90"]
                                                 - self.ans_df.loc[row, "amortizacion90"]
                                                 - self.ans_df.loc[row, "prepago90"]
                                                 - self.ans_df.loc[row, "castigo90"])
        self.ans_df.loc[row, "saldo_final120"] = (self.ans_df.loc[row, "saldo_inicial120"]
                                                  - self.ans_df.loc[row, "amortizacion120"]
                                                  - self.ans_df.loc[row, "prepago120"]
                                                  - self.ans_df.loc[row, "castigo120"])
        self.ans_df.loc[row, "saldo_final150"] = (self.ans_df.loc[row, "saldo_inicial150"]
                                                  - self.ans_df.loc[row, "amortizacion150"]
                                                  - self.ans_df.loc[row, "prepago150"]
                                                  - self.ans_df.loc[row, "castigo150"])
        self.ans_df.loc[row, "saldo_final180"] = (self.ans_df.loc[row, "saldo_inicial180"]
                                                  - self.ans_df.loc[row, "amortizacion180"]
                                                  - self.ans_df.loc[row, "prepago180"]
                                                  - self.ans_df.loc[row, "castigo180"])
        self.ans_df.loc[row, "saldo_final210"] = (self.ans_df.loc[row, "saldo_inicial210"]
                                                  - self.ans_df.loc[row, "amortizacion210"]
                                                  - self.ans_df.loc[row, "prepago210"]
                                                  - self.ans_df.loc[row, "castigo210"])


    def _prepago_por_calificacion(self, row):
        """
        Obtiene el valor % de prepago que aplica para una edad y calificacion
        aplica el factor de prepago a cada saldo inicial de acuerdo a su calificacion
        actualiza el dataframe de salida

        """
        prepago_por_edad = self._vector_prepago[self.ans_df.index.get_loc(row)]
        a = self._percent_prepago_por_calificacion * prepago_por_edad
        b = self.get_saldo_inicial(row)
        c = a * b

        # actualizar el dataframe de salida
        self.ans_df.loc[row, "prepago0"] = c.get_value(0)
        self.ans_df.loc[row, "prepago30"] = c.get_value(30)
        self.ans_df.loc[row, "prepago60"] = c.get_value(60)
        self.ans_df.loc[row, "prepago90"] = c.get_value(90)
        self.ans_df.loc[row, "prepago120"] = c.get_value(120)
        self.ans_df.loc[row, "prepago150"] = c.get_value(150)
        self.ans_df.loc[row, "prepago180"] = c.get_value(180)
        self.ans_df.loc[row, "prepago210"] = c.get_value(210)


    def _castigo_por_calificacion(self, row):
        """
        obtiene el % de castigo para cada calificacion
        aplica el factor de castigo a cada saldo inicial de acuerdo a su calificacion
        actualiza el dataframe de salida
        """
        a = self._percent_castigo_por_calificacion
        b = self.get_saldo_inicial(row)
        c = a * b

        # actualizar el dataframe de salida
        self.ans_df.loc[row, "castigo0"] = c.get_value(0)
        self.ans_df.loc[row, "castigo30"] = c.get_value(30)
        self.ans_df.loc[row, "castigo60"] = c.get_value(60)
        self.ans_df.loc[row, "castigo90"] = c.get_value(90)
        self.ans_df.loc[row, "castigo120"] = c.get_value(120)
        self.ans_df.loc[row, "castigo150"] = c.get_value(150)
        self.ans_df.loc[row, "castigo180"] = c.get_value(180)
        self.ans_df.loc[row, "castigo210"] = c.get_value(210)


    def _estructura_temporal_cartera(self):
        """
        construye un diccionario con la estructura temporal de la cartera por calificacion
        aplicando la matriz de transicion para cada periodo

        """
        # crea un diccionario vacio con n keys desde la fecha desde la originacion
        dates_index = pd.date_range(self.fecha_originacion(), periods = self._max_forecast, freq = 'M')
        ans_dict = dict.fromkeys(dates_index)

        for key in dates_index:
            if key == dates_index[0]:
                # mes cero, desembolso
                ans_dict[dates_index[0]] = pd.Series([1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                                                     index = self._alturas_mora)
                # aplicar transicion y actualizar t+1
                m = self._matriz_de_transicion(key)
                ans = pd.Series(np.dot(np.transpose(m), ans_dict[key]),
                                index = self._alturas_mora)
                ans_dict[key + 1 ] = ans


            else:
                m = self._matriz_de_transicion(key)
                ans = pd.Series(np.dot(np.transpose(m), ans_dict[key]),
                                index = self._alturas_mora)
                ans_dict[key + 1 ] = ans

        # TODO: refactoring para no repetir instrucciones
        return ans_dict


    def _tasas_full_nmv(self):
        """
        Computa la tasa full nmv para cada periodo basado en las caracteristicas
        faciales del producto
        """
        # TODO: implementar diferentes indices
        # TODO: implementar reprecio
        if self._tipo_tasa == "FIJA":
            return self._spread_originacion.apply(lambda x: (1 + x) ** (1 / 12) - 1)
        elif self._tipo_tasa == "DTF":
            pass
        elif self._tipo_tasa == "IPC":
            pass
        elif self._tipo_tasa == "IBR":
            pass


    def _amortizacion_por_calificacion(self, row):
        """
        Computa el valor de amortizacion para un credito, dadas unas condiciones faciales

        """
        k = self.estructura_temporal[row] * self._desembolso
        i = self.tasas_nmv.get_value(row)
        nper = self._plazo
        per = row.to_period('M') - self._fecha_originacion.to_period('M')

        ans = pd.Series(0.0, index = self._alturas_mora)

        # calcular el pago de principal para cada calificacion
        if per > 0:
            for index, val in k.iteritems():
                ppay = np.abs(np.ppmt(i, per, nper, val, 0))
                ans.set_value(index, ppay)

        # ajustar por la probabilidad de pago dada altura de mora
        ans = ans * self._percent_amortizacion_por_calificacion





        # actualizar el dataframe de salida
        # debe verificar que el valor a amortizar existe despues de castigo y prepago
        self.ans_df.loc[row, "amortizacion0"] = min((self.ans_df.loc[row, "saldo_inicial0"]
                                                - self.ans_df.loc[row, "prepago0"]
                                                - self.ans_df.loc[row, "castigo0"]),
                                               ans.get_value(0))
        self.ans_df.loc[row, "amortizacion30"] = min((self.ans_df.loc[row, "saldo_inicial30"]
                                                - self.ans_df.loc[row, "prepago30"]
                                                - self.ans_df.loc[row, "castigo30"]),
                                               ans.get_value(30))
        self.ans_df.loc[row, "amortizacion60"] = min((self.ans_df.loc[row, "saldo_inicial60"]
                                                - self.ans_df.loc[row, "prepago60"]
                                                - self.ans_df.loc[row, "castigo60"]),
                                               ans.get_value(60))
        self.ans_df.loc[row, "amortizacion90"] = min((self.ans_df.loc[row, "saldo_inicial90"]
                                                - self.ans_df.loc[row, "prepago90"]
                                                - self.ans_df.loc[row, "castigo90"]),
                                               ans.get_value(90))
        self.ans_df.loc[row, "amortizacion120"] = min((self.ans_df.loc[row, "saldo_inicial120"]
                                                - self.ans_df.loc[row, "prepago120"]
                                                - self.ans_df.loc[row, "castigo120"]),
                                               ans.get_value(120))
        self.ans_df.loc[row, "amortizacion150"] = min((self.ans_df.loc[row, "saldo_inicial150"]
                                                - self.ans_df.loc[row, "prepago150"]
                                                - self.ans_df.loc[row, "castigo150"]),
                                               ans.get_value(150))
        self.ans_df.loc[row, "amortizacion180"] = min((self.ans_df.loc[row, "saldo_inicial180"]
                                                - self.ans_df.loc[row, "prepago180"]
                                                - self.ans_df.loc[row, "castigo180"]),
                                               ans.get_value(180))
        self.ans_df.loc[row, "amortizacion210"] = min((self.ans_df.loc[row, "saldo_inicial210"]
                                                - self.ans_df.loc[row, "prepago210"]
                                                - self.ans_df.loc[row, "castigo210"]),
                                               ans.get_value(210))


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
        update end constructor_de_balance of month 0 as beginning constructor_de_balance month 1
        """

        vector_saldo_final = self.get_saldo_final(row)

        vector_final_con_transicion = np.dot(np.transpose(self._matriz_de_transicion(row)),
                                            vector_saldo_final)

        self._actualizar_saldo_inicial(row + 1, vector_final_con_transicion)


    def _actualizar_saldo_inicial(self, row, vector_final_con_transicion):
        """
        Actualiza el saldo inicial de un periodo como el saldo final del
        periodo anterior aplicada la matriz de transicion por calificacion
        """
        self.ans_df.loc[row, "saldo_inicial0"] = vector_final_con_transicion[0]
        self.ans_df.loc[row, "saldo_inicial30"] = vector_final_con_transicion[1]
        self.ans_df.loc[row, "saldo_inicial60"] = vector_final_con_transicion[2]
        self.ans_df.loc[row, "saldo_inicial90"] = vector_final_con_transicion[3]
        self.ans_df.loc[row, "saldo_inicial120"] = vector_final_con_transicion[4]
        self.ans_df.loc[row, "saldo_inicial150"] = vector_final_con_transicion[5]
        self.ans_df.loc[row, "saldo_inicial180"] = vector_final_con_transicion[6]
        self.ans_df.loc[row, "saldo_inicial210"] = vector_final_con_transicion[7]


    def get_saldo_final(self, row):
        """
        Obtiene una serie de saldos finales ordenados por calificacion
        """

        return pd.Series([self.ans_df.loc[row, "saldo_final0"],
                          self.ans_df.loc[row, "saldo_final30"],
                          self.ans_df.loc[row, "saldo_final60"],
                          self.ans_df.loc[row, "saldo_final90"],
                          self.ans_df.loc[row, "saldo_final120"],
                          self.ans_df.loc[row, "saldo_final150"],
                          self.ans_df.loc[row, "saldo_final180"],
                          self.ans_df.loc[row, "saldo_final210"]],
                         index = self._alturas_mora)


    def get_saldo_inicial(self, row):
        """
        Obtiene una serie de saldos iniciales ordenados por calificacion
        """

        return pd.Series([self.ans_df.loc[row, "saldo_inicial0"],
                          self.ans_df.loc[row, "saldo_inicial30"],
                          self.ans_df.loc[row, "saldo_inicial60"],
                          self.ans_df.loc[row, "saldo_inicial90"],
                          self.ans_df.loc[row, "saldo_inicial120"],
                          self.ans_df.loc[row, "saldo_inicial150"],
                          self.ans_df.loc[row, "saldo_inicial180"],
                          self.ans_df.loc[row, "saldo_inicial210"]],
                         index = self._alturas_mora)



def print_cosecha(cosecha):
    """
    Print nicely the vintage results
    :param: vintage: credit vintage object
    :return: console output
    """
    from tabulate import tabulate
    print(tabulate(cosecha,
                   headers = 'keys',
                   numalign = 'right',
                   tablefmt = 'psql',
                   floatfmt = ",.3f"))





if __name__ == '__main__':


    x1 = Cosecha_Credito(settings_cosecha())
    balance = x1.constructor_de_balance()
    print_cosecha(balance)

    # writer = pd.ExcelWriter('\\git\banking\data\cosecha.xlsx')
    # balance.to_excel(writer)
    # writer.save()
