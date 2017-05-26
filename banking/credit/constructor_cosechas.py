
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
# from decimal import Decimal, getcontext, ROUND_HALF_DOWN
from develop_testing.pruebas1 import *


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
        self._frecuencia_reprecio = settings['frecuencia_reprecio']
        self._plazo = settings['plazo']
        self._fecha_originacion = pd.to_datetime(settings['fecha_originacion'])
        self._desembolso = settings['desembolso']

        self._vector_tasas_indice = settings['vector_tasas_indice']
        self._tasa_originacion = settings['tasa_originacion']

        self._vector_prepago = settings['vector_prepago']

        self._matrices_transcicion = settings['matrices_transicion']
        self._recaudo_por_calificacion = settings['recaudo_por_calificacion']
        self._castigo_por_calificacion = settings['castigo_por_calificacion']
        self._provision_por_calificacion = settings['provision_por_calificacion']

        # crear estructura de salida
        self.ans_df = self._df_structure()


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


    def _df_structure(self):
        """
        Crea la estructura del dataframe de salida
        :return pandas dataframe
        """

        dates_index = pd.date_range(self.fecha_originacion(), periods = self.plazo(), freq = 'M')

        return pd.DataFrame(0.0,
                            index = dates_index,
                            columns = ('saldo_inicial0', 'saldo_inicial30', 'saldo_inicial60',
                            'saldo_inicial90', 'saldo_inicial120', 'saldo_inicial150',
                            'saldo_inicial180', 'saldo_inicial210',
                            'desembolso0',
                            'recaudo0', 'recaudo30', 'recaudo60', 'recaudo90',
                            'recaudo120', 'recaudo150', 'recaudo180', 'recaudo210',
                            'prepago0', 'prepago30', 'prepago60', 'prepago90',
                            'prepago120', 'prepago150', 'prepago180', 'prepago210',
                            'castigo0', 'castigo30', 'castigo60', 'castigo90',
                            'castigo120', 'castigo150', 'castigo180', 'castigo210',
                            'saldo_final0', 'saldo_final30', 'saldo_final60', 'saldo_final90',
                            'saldo_final120', 'saldo_final150', 'saldo_final180',
                            'saldo_final210'))


    def balance(self):
        #=======================================================================
        # Construct a dataframe with projections of balances and cash flows for
        # a loan portfolio in an homogeneous loan pool, where the loans share
        # the same origination period.
        #=======================================================================

        # iterar cada fila
        for row, col in self.ans_df.iterrows():
            # hacer desembolso en t+0
            if row == self.fecha_originacion():
                self.ans_df.loc[self._fecha_originacion, 'desembolso0'] = self._desembolso


            # actualizar saldos finales sin amortizacion y castigos
            self.ans_df.loc[row, "saldo_final0"] = self.ans_df.loc[row, "saldo_inicial0"] + self.ans_df.loc[row, "desembolso0"]
            self.ans_df.loc[row, "saldo_final30"] = self.ans_df.loc[row, "saldo_inicial30"]
            self.ans_df.loc[row, "saldo_final60"] = self.ans_df.loc[row, "saldo_inicial60"]
            self.ans_df.loc[row, "saldo_final90"] = self.ans_df.loc[row, "saldo_inicial90"]
            self.ans_df.loc[row, "saldo_final120"] = self.ans_df.loc[row, "saldo_inicial120"]
            self.ans_df.loc[row, "saldo_final150"] = self.ans_df.loc[row, "saldo_inicial150"]
            self.ans_df.loc[row, "saldo_final180"] = self.ans_df.loc[row, "saldo_inicial180"]
            self.ans_df.loc[row, "saldo_final210"] = self.ans_df.loc[row, "saldo_inicial210"]



            # aplicar matriz de transicion
            vector_final = self.vector_saldo_final(row, self.ans_df)
            vector_final_con_transicion = self.aplicar_transicion(row + 1, vector_final)
            # actualizar dataframe
            self.actualizar_saldo_inicial(row + 1, vector_final_con_transicion)


 
        return self.ans_df








    def actualizar_saldo_inicial(self, row, vector_inicial1):
        # print_cosecha(self.ans_df)
        self.ans_df.loc[row, "saldo_inicial0"] = vector_inicial1[0]
        self.ans_df.loc[row, "saldo_inicial30"] = vector_inicial1[1]
        self.ans_df.loc[row, "saldo_inicial60"] = vector_inicial1[2]
        self.ans_df.loc[row, "saldo_inicial90"] = vector_inicial1[3]
        self.ans_df.loc[row, "saldo_inicial120"] = vector_inicial1[4]
        self.ans_df.loc[row, "saldo_inicial150"] = vector_inicial1[5]
        self.ans_df.loc[row, "saldo_inicial180"] = vector_inicial1[6]
        self.ans_df.loc[row, "saldo_inicial210"] = vector_inicial1[7]


    def matriz_de_transicion(self, row):
        #===========================================================================
        # locate the right transition matrix for the period.
        # If not a correct matrix is found, look up for month = 1 else
        # will give keyerror
        #===========================================================================

        if row.month in self._matrices_transcicion.keys():
            return self._matrices_transcicion[row.month]
        else:
            return self._matrices_transcicion[1]


    def vector_saldo_final(self, row, df):
        #===============================================================================
        # Creates a list for the end of month balance for each delinquency
        #===============================================================================
        return [df.loc[row, "saldo_final0"],
                df.loc[row, "saldo_final30"],
                df.loc[row, "saldo_final60"],
                df.loc[row, "saldo_final90"],
                df.loc[row, "saldo_final120"],
                df.loc[row, "saldo_final150"],
                df.loc[row, "saldo_final180"],
                df.loc[row, "saldo_final210"]]


    def aplicar_transicion(self, row, vector_input):
        #=======================================================================
        # Apply a transition matrix to a vector of balances for delinquency,
        # return a vector of balances after transition
        #=======================================================================
        m = np.transpose(self.matriz_de_transicion(row))
        return  np.dot(m, vector_input)


def print_cosecha(cosecha):
    """
    Print nicely the vintage results
    :param vintage: credit vintage object
    :return: console output
    """
    from tabulate import tabulate
    print(tabulate(cosecha,
                   headers = 'keys',
                   numalign = 'right',
                   tablefmt = 'psql',
                   floatfmt = ",.0f"))





if __name__ == '__main__':

    # correr_constructor_antiguo()
    # pprint.pprint(pruebas1.settings_cosecha())

    x1 = Cosecha_Credito(settings_cosecha())
    print_cosecha(x1.balance())
