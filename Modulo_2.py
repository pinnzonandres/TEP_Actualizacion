# Cargamos las librerias necesarias
import pandas as pd

# Se define un  Diccionario para añadir el mes de cada fila
month_dict = {1: 'Enero', 2: 'Febrero', 3: 'Marzo', 
              4: 'Abril', 5: 'Mayo', 6: 'Junio', 
              7: 'Julio', 8: 'Agosto', 9: 'Septiembre',
              10: 'Octubre', 11: 'Noviembre', 12:'Diciembre'} 

## Función para añdir los meses y su respectivo No. Mes
def _month_add(data: pd.DataFrame, col: str) -> pd.DataFrame:
    """
    Esta función agrega los meses y su respectivo número de mes a un dataframe de Pandas.

    Args:
    data: El dataframe a modificar.
    col: La columna que contiene las fechas.

    Returns:
    Un dataframe de Pandas con los meses y su respectivo número de mes agregados.
    """

    # Convertimos la columna a formato datetime.
    data[col] = pd.to_datetime(data[col])

    # Agregamos una columna con el número de mes.
    data['No. Mes'] = data[col].dt.month

    # Agregamos una columna con el nombre del mes.
    data['Mes'] = data['No. Mes'].replace(month_dict)

    # Devolvemos el dataframe.
    return data

# Función que permite agrupar los datos en cuestión de las columnas necesarias
def agrupar_mes(data: pd.DataFrame, valor: str, Nombre_columna: str) -> pd.DataFrame:
    """
    Esta función agrupa un dataframe de Pandas por mes y recurso, y luego calcula el total de la columna `valor`.

    Args:
        data: El dataframe a modificar.
        valor: La columna que se va a sumar.
        Nombre_columna: El nombre de la nueva columna que se va a crear.

    Returns:
        Un dataframe de Pandas con los datos agrupados por mes y recurso, y con la columna `valor` sumada.
    """
    # Agrupamos el dataframe por rubro, mes y tipo de recurso
    gr = data.groupby(by=['Index_Rubro','Mes','Recurso'], as_index=False).agg({
        valor:'sum',
        'Dirección':'first',
        'Descripción Rubro': 'first',
        'No. Mes': 'first'
        })
    
    # Se renombra la columna calculada por el nombre deseado desde el argumento
    gr = gr.rename(columns={valor : Nombre_columna})
    
    # Devolvemos el dataframe resultante
    return gr


# Se define una función que permite crear el reporte acumulado mensual de cada programa de la dirección
def get_pre_second_base(RG: pd.DataFrame, CDP: pd.DataFrame, RP: pd.DataFrame, OB: pd.DataFrame, OP: pd.DataFrame, month: int) -> pd.DataFrame:
    """
    Esta función obtiene el dataframe base para el segundo nivel de análisis.

    Args:
        RG: El dataframe de nivel general.
        CDP: El dataframe de certificados de disponibilidad presupuestal.
        RP: El dataframe de compromisos.
        OB: El dataframe de obligaciones.
        OP: El dataframe de órdenes de pago.
        month: El mes máximo sobre el que se va a crear el dataframe.

    Returns:
        El dataframe base para el segundo nivel de análisis.
    """
    
    ## Seleccionamos las columnas que necesitamos unicamente del reporte de ejecución agregada inicial
    GENERAL = RG.iloc[:,[0,1,2,3,7]]
    
    ## Creamos un dataframe donde guardamos la información del dataframe original para cada mes
    result = pd.DataFrame()
    for i in month_dict.keys():
        if i <= month:
            df = GENERAL
            df.loc[:, 'No. Mes'] = i
            df.loc[:,'Mes'] = month_dict[i]
            result = pd.concat([result,df]).reset_index(drop=True)
            
    ## Filtramos las ordenes de pago solo por aquellas que ya están pagadas para quitar las únicamente creadas
    OP = OP[OP['Estado']=='Pagada'].reset_index(drop = True)
    
    ### Añadimos la columna de mes para cada base de datos
    CDP = _month_add(CDP, 'Fecha de Creacion')
    RP = _month_add(RP, 'Fecha de Creacion')
    OB = _month_add(OB, 'Fecha de Creacion')
    OP = _month_add(OP, 'Fecha de pago')
    
    ## Agrupamos nuestros datos para tener la información agrupada por cada uno de los meses en la columna preestablecida
    GCDP = agrupar_mes(CDP, 'Valor Actual', 'Valor CDP')
    GRP = agrupar_mes(RP, 'Valor Actual', 'Valor RP')
    GOB = agrupar_mes(OB, 'Valor Actual.1', 'Valor OB')
    GOP = agrupar_mes(OP, 'Valor Neto Pesos', 'Valor OP')
    
    ## Añadimos cada columna a nuestra base de datos
    result = result.merge(GCDP, how ='left', on = ['Index_Rubro', 'Mes','Dirección','Descripción Rubro','Recurso', 'No. Mes'])
    result = result.merge(GRP, how ='left', on = ['Index_Rubro', 'Mes','Dirección','Descripción Rubro','Recurso', 'No. Mes'])
    result = result.merge(GOB, how ='left', on = ['Index_Rubro', 'Mes','Dirección','Descripción Rubro','Recurso', 'No. Mes'])
    result = result.merge(GOP, how ='left', on = ['Index_Rubro', 'Mes','Dirección','Descripción Rubro','Recurso', 'No. Mes'])
    result.fillna(0, inplace = True)
    
    
    ## Hacemos la suma acumulada para tener el resultado acumulado por cada mes
    result['CDP Acumulado'] = result.groupby(['Index_Rubro','Recurso'])['Valor CDP'].cumsum(numeric_only=True)
    result['RP Acumulado'] = result.groupby(['Index_Rubro','Recurso'])['Valor RP'].cumsum(numeric_only=True)
    result['OB Acumulado'] = result.groupby(['Index_Rubro','Recurso'])['Valor OB'].cumsum(numeric_only=True)
    result['OP Acumulado'] = result.groupby(['Index_Rubro','Recurso'])['Valor OP'].cumsum(numeric_only=True)
    
    # Se devuelve el dataframe resultante:
    return result


# Función para el análisis de los RP
def get_pre_re_second_base(RP: pd.DataFrame, OB: pd.DataFrame, OP: pd.DataFrame, month: int) -> pd.DataFrame:
    """
    Esta función obtiene el dataframe base para el análisis de los RP contra las obligaciones y ordenes de pago.

    Args:
    RP: El dataframe de los compromisos.
    OB: El dataframe de las obligaciones.
    OP: El dataframe de órdenes de pago.
    month: El mes en el que se quiere obtener el dataframe.

    Returns:
    El dataframe base para el segundo nivel de análisis.
    """
    # Agrupamos la base del reporte agregado por el rubro y tipo de recurso
    RPG = RP.groupby(by=['Index_Rubro','Recurso'], as_index = False).agg({
        'Valor Actual':'sum',
        'Dirección':'first',
        'Descripción Rubro': 'first'
        })
    
    ## Creamos un dataframe donde guardamos la información del dataframe original para cada mes
    result = pd.DataFrame()
    for i in month_dict.keys():
        if i <= month:
            df = RPG
            df.loc[:, 'No. Mes'] = i
            df.loc[:,'Mes'] = month_dict[i]
            result = pd.concat([result,df]).reset_index(drop=True)
            
    ## Filtramos las ordenes de pago solo por aquellas que ya están pagadas para quitar las únicamente creadas
    OP = OP[OP['Estado']=='Pagada'].reset_index(drop = True)
    
    ### Añadimos la columna de mes para cada base de datos
    OB = _month_add(OB, 'Fecha de Creacion')
    OP = _month_add(OP, 'Fecha de pago')
    
    ## Agrupamos nuestros datos para tener la información agrupada por cada uno de los meses en la columna preestablecida
    GOB = agrupar_mes(OB, 'Valor Actual.1', 'Valor OB')
    GOP = agrupar_mes(OP, 'Valor Neto Pesos', 'Valor OP')
    
    # Hacemos la unión de la base generada de cada mes con los reportes de obligaciones y pagos por cada mes
    result = result.merge(GOB, how ='left', on = ['Index_Rubro', 'Mes','Dirección','Descripción Rubro','Recurso', 'No. Mes'])
    result = result.merge(GOP, how ='left', on = ['Index_Rubro', 'Mes','Dirección','Descripción Rubro','Recurso', 'No. Mes'])
    
    # Reemplazamos los valores nulos por el valor de 0 para evitar conflictos en la lectura de las columnas
    result.fillna(0, inplace = True)
    
    
    ## Hacemos la suma acumulada para tener el resultado acumulado por cada mes
    result['OB Acumulado'] = result.groupby(['Index_Rubro','Recurso'])['Valor OB'].cumsum(numeric_only=True)
    result['OP Acumulado'] = result.groupby(['Index_Rubro','Recurso'])['Valor OP'].cumsum(numeric_only=True)
    
    # Devolvemos el dataframe resultante
    return result