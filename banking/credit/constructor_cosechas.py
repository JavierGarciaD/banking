


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
                              columns=('saldo_inicial30', 'saldo_inicial60', 'saldo_inicial90',
                                       'saldo_inicial120', 'saldo_inicial150',
                                       'saldo_inicial180', 'saldo_inicial210',
                                       'desembolso30',
                                       'recaudo30', 'recaudo60',
                                       'recaudo90', 'recaudo120',
                                       'recaudo150', 'recaudo180',
                                       'recaudo210',
                                       'prepago30', 'prepago60',
                                       'prepago90', 'prepago120',
                                       'prepago150', 'prepago180',
                                       'prepago210',
                                       'castigo30', 'castigo60',
                                       'castigo90', 'castigo120',
                                       'castigo150', 'castigo180',
                                       'castigo210',
                                       'saldo_final30', 'saldo_final60',
                                       'saldo_final90', 'saldo_final120',
                                       'saldo_final50', 'saldo_final180',
                                       'saldo_final210',
                                       'interes30', 'interes60',
                                       'interes90', 'interes120',
                                       'interes150', 'interes180',
                                       'interes210'))
                                       
        
        return ans_df


