


import numpy as np
import pandas as pd


class Cosecha_Credito:
    #===========================================================================
    # Construct an object with information for a loan portfolio on
    # an homogeneous loan pool, where the loans share the same origination period. 
    #===========================================================================
        
    def __init__(self, settings):
        """
        Init
        """
        # 
        self._producto = settings['producto']
        self._tipo_tasa = settings['tipo_tasa']
        self._plazo = settings['plazo']
        self._fecha_originacion = settings['fecha_originacion']
        self._desembolso = settings['desembolso']
        
        self._vector_tasas_indice = settings['vector_tasas_indice']
        self._tasa_originacion = settings['tasa_originacion']
        
        self._vector_prepago = settings['vector_prepago']
        
        self._matrices_transcicion_inventario = settings['matrices_transicion_inventario']
        self._matrices_transcicion_nuevo = settings['matrices_transicion_nuevo']
        self._recaudo_por_calificacion = settings['recaudo_por_calificacion']
        self._castigo_por_calificacion = settings['castigo_por_calificacion']
        self._provision_por_calificacion = settings['provision_por_calificacion']
        
        
        
        
    def flujo_de_caja(self):
        #=======================================================================
        # Construct a dataframe with projections of balances and cash flows for 
        # a loan portfolio in an homogeneous loan pool, where the loans share
        # the same origination period.
        #=======================================================================
        
        
        ans_df = pd.DataFrame(0.,
                              index=index_to_apply,
                              columns=('saldo_inicial30',
                                       'desembolso',
                                       'recaudo',
                                       'prepago',
                                       'castigo',
                                       'saldo_final',
                                       'interes',
                                       'improductiva'))
        
        return ans_df