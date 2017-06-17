"""
Created on 9/06/2017

@author: spectre
"""
import pandas as pd
import numpy as np


class Provision():
    """
    Construct an object with information for the provisions for a loan
    portfolio
    on an homogeneous loan pool, where the loans share the same origination
    period.
    """

    def __init__(self, cosecha, prov_calif):

        self._rounding = 2

        self.cosecha = cosecha
        self.prov_calif = prov_calif

        # crear estructuras necesarias
        self.ans_df = self._df_structure()
        self._constructor_de_balance()

    def _df_structure(self):
        """
        Crea la estructura del dataframe de salida
        :return pandas dataframe
        """

        return pd.DataFrame(0.0, index=self.cosecha.get_index(), columns=(
            'saldo_inicial0', 'saldo_inicial30', 'saldo_inicial60',
            'saldo_inicial90', 'saldo_inicial120', 'saldo_inicial150',
            'saldo_inicial180', 'saldo_inicial210', 'gasto0', 'gasto30',
            'gasto60', 'gasto90', 'gasto120', 'gasto150', 'gasto180',
            'gasto210', 'castigo0', 'castigo30', 'castigo60', 'castigo90',
            'castigo120', 'castigo150', 'castigo180', 'castigo210',
            'saldo_final0', 'saldo_final30', 'saldo_final60', 'saldo_final90',
            'saldo_final120', 'saldo_final150', 'saldo_final180',
            'saldo_final210'))

    def _constructor_de_balance(self):
        """
        Computa provisiones por calificacion
        """
        self._actualizar_saldo_final()
        self._actualizar_saldo_inicial()
        self._actualizar_castigo()
        self._actualizar_gasto()

    def _actualizar_saldo_final(self):
        """
        Computa el saldo final de provision para cada nivel de calificacion
        tomando el saldo final de la cosecha en cada periodo
        """
        saldos = self.cosecha.get_serie(serie_name="saldo_final",
                                        per_score =True)

        for key, val in self.prov_calif.items():
            self.ans_df["saldo_final" + str(key)] = np.round(
                    saldos["saldo_final" + str(key)] * val, self._rounding)

    def _actualizar_saldo_inicial(self):
        """
        Actualiza el saldo inicial.
        saldo inicial t+0  = 0.0,
        saldo inicial t+1 = saldo inicial+0
        """
        for key in self.prov_calif:
            self.ans_df["saldo_inicial" + str(key)] = self.ans_df[
                "saldo_final" + str(key)].shift(1)
        self.ans_df.fillna(0.0, inplace=True)

    def _actualizar_castigo(self):
        """
        castigos pasan igual desde la cosecha

        """
        castigos = self.cosecha.get_serie(serie_name="castigo", per_score =True)
        for key in self.prov_calif:
            self.ans_df["castigo" + str(key)] = np.round(
                    castigos["castigo" + str(key)], self._rounding)

    def _actualizar_gasto(self):
        """
        castigo = saldo final - saldo inicial + castigo
        """
        for key in self.prov_calif:
            self.ans_df["gasto" + str(key)] = np.round((self.ans_df[
                                                            "saldo_final" +
                                                            str(
                                                                key)] -
                                                        self.ans_df[
                                                            "saldo_inicial"
                                                            + str(
                                                                    key)] +
                                                        self.ans_df[
                                                            "castigo" + str(
                                                                    key)]),
                                                       self._rounding)

    def get_balance(self, por_calif=False):
        """
        Construye el balance de la cosecha y lo exporta a un df
        se puede elegir entre vista por calificacion o vista agregada
        """
        if por_calif == True:
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
            ans = self.ans_df["desembolso0"]
            por_calif = True
        else:
            ans = self.ans_df[[serie_name + str(0), serie_name + str(30),
                               serie_name + str(60), serie_name + str(90),
                               serie_name + str(120), serie_name + str(150),
                               serie_name + str(180), serie_name + str(210)]]

        if por_calif == True:
            return ans
        else:
            return ans.sum(axis=1)
