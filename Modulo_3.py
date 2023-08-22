'''
- Script Modulo_3.py
- Script encargado de realizar la base relacionada de obligaciones y giros totales por cada compromiso
- Autor: Wilson Andrés Pinzón (wilson.pinzon@prosperidadsocial.gov.co)
- Fecha_Actualización: 23/08/22
'''

# Cargamos las librerias necesarias
import pandas as pd

# Función para realizar el dataframe comparativo entre  los RP, Obligaciones y órdenes de pago
def get_third_base(RP: pd.DataFrame, OB: pd.DataFrame, OP: pd.DataFrame) -> pd.DataFrame:
    """
    Esta función obtiene el dataframe para el análisis de cada RP respecto a sus obligaciones y órdenes de pago

    Args:
    RP: El dataframe de RP.
    OB: El dataframe de obligaciones.
    OP: El dataframe de órdenes de pago.

    Returns:
    El dataframe base para el tercer nivel de análisis.
    """
    # Filtramos las ordenes de pago solo por aquellas que ya están pagadas
    OP = OP[OP['Estado']=='Pagada'].reset_index(drop = True)
    
    # Agrupamos el dataframe de compromisos por el número de compromiso el rubro asociado y el tipo de recurso
    GRP = RP.groupby(by = ['Compromisos','Index_Rubro','Recurso'], as_index = False).agg({
        'Fecha de Creacion':'first',
        'Estado':'first',
        'Dependencia' : 'first',
        'Dependencia Descripcion':'first',
        'Fuente' : 'first',
        'Valor Inicial': 'sum',
        'Valor Operaciones': 'sum',
        'Valor Actual': 'sum',
        'Saldo por Utilizar':'sum',
        'Tipo Identificacion': 'first',
        'Nombre Razon Social': 'first',
        'CDP':'first',
        'Obligaciones':'first',
        'Ordenes de Pago' : 'first',
        'Fecha Documento Soporte': 'first',
        'Tipo Documento Soporte': 'first',
        'Numero Documento Soporte' : 'first',
        'Observaciones': 'first',
        'Descripción Rubro':'first',
        'Dirección':'first'
        })
    
    # Agrupamos el dataframe de obligaciones por índice de rubro y recurso
    GOB= OB.groupby(by = ['Compromisos','Index_Rubro','Recurso'], as_index = False).agg({'Valor Actual.1': 'sum'})
    
    # Renombramos la columna `Valor Actual.1` a `Valor Obligaciones`
    GOB = GOB.rename(columns = {'Valor Actual.1':'Valor Obligaciones'})
    
    # Agrupamos el dataframe de órdenes de pago por índice de rubro y recurso
    GOP = OP.groupby(by = ['Compromisos','Index_Rubro','Recurso'], as_index = False).agg({'Valor Neto Pesos': 'sum'})
    
    # Renombramos la columna `Valor Neto Pesos` a `Valor Ordenes de Pago`
    GOP = GOP.rename(columns = {'Valor Neto Pesos': 'Valor Ordenes de Pago'})
    
    # Combinamos los tres dataframe en uno.
    result = GRP.merge(GOB, how = 'left', on = ['Compromisos','Index_Rubro','Recurso'])
    result = result.merge(GOP, how = 'left', on = ['Compromisos', 'Index_Rubro','Recurso'])
    
    # Creamos una nueva columna `Tipo Contratista` que clasifica los contratistas en personas naturales o jurídicas.
    result['Tipo Contratista'] = result['Tipo Identificacion'].apply(lambda x: 'Persona natural' if x =='Cédula de Ciudadanía' else 'Persona jurídica')
    
    # Devolvemos el dataframe resultante
    return result

