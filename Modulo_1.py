# Se importan las liberias necesarias
import pandas as pd

# Función para poder cambiar todas las columnas númericas que están en formato de texto con comas a su valor númerico
# En la función debe ingresar un dataframe y una lista con el nombre de las columnas a las que se les va a realizar el cambio
def str_to_float(data:pd.DataFrame, columnas: list):
    for i in columnas:
        # Para cada columna se toma el valor de tipo texto, se elimminan los valores de coma y se convierte en un dato numérico de tipo float
        data[i] = data[i].apply(lambda x: float(str(x).replace(",","")))
    return data

# Función para concatenar las bases de datos del mismo tipo de ejecución cuyo recurso es de la Entidad y de FIP
# En la función ingresan dos dataframes
def unificar_data(data1: pd.DataFrame, data2:pd.DataFrame)-> pd.DataFrame:
    """
        Esta función une dos dataframes de Pandas.

        Args:
        data1: El primer dataframe.
        data2: El segundo dataframe.

        Returns:
        El dataframe con los dos dataframes unidos.
    """
    
    ## Eliminamos aquellas columnas vacias que no tienen información
    data1 = data1.dropna(subset=data1.columns[0]).reset_index(drop = True)
    data2 = data2.dropna(subset=data2.columns[0]).reset_index(drop = True)
    
    # Guardamos la información de los nombres de las columnas y lo convertimos en un diccionario para luego realizar un cambio de nombre de columnas con
    # tal que estan seán iguales y se puedan concatenar las tablas sobre las mismas columnas
    n_data1 = list(data1.columns)
    n_data2 = list(data2.columns)
    names = {n_data2[i]:n_data1[i] for i in range(len(n_data1))}
    
    # Reemplazamos los nombres de las columnas del dataframe de FIP con los nombre de las columnas del dataframe de DPS
    data2 = data2.rename(columns = names)
    
    # Concatenamos las bases de datos
    result = pd.concat([data1, data2]).reset_index(drop = True)
    
    # La función devuelve el dataframe con la concatenación de los dos dataframes
    return result


# Se definen varios diccionarios con información base para la creación de las columnas de programa y dirección
## Diccionario con la relación del nombre de cada programa según el rubro presupuestal 
rubro_names = {'13':"ReSA",
               '14':'Infraestructura',
              '16':"Política de Seguridad Alimentaria",
              '17':"Inclusión Productiva",
              '21':"IRACA",
              '22':"FEST",
              '25':'Generación de Ingresos',
              '12':'Transferencias Monetarias Condicionadas',
              '20':'Transferencias Monetarias no Condicionadas',
              '23':'Colombia Mayor'}

## Diccionario con la información de los rubros presupuestales que pertenecen a cada dirección
dir_names = {'Inclusión Productiva':['13','16','17','21','22','25'],
        'Infraestructura Social y Habitat':['14'],
        'Transferencias Monetarias':['12','20','23']}

# Función para encontrar el valor del key asociado a un valor en un diccionario
def find_key(dictionary, value):
    for key, values in dictionary.items():
        if value in values:
            return key
    return None

# Función para añadir el rubro y la dirección a un dataframe
def filter_rubros(data: pd.DataFrame)-> pd.DataFrame:
    """
        Esta función filtra los datos del dataframe de acuerdo con los rubros especificados.

        Args:
            data: El dataframe de Pandas.

        Returns:
            Un dataframe de Pandas con los datos filtrados.
    """
    
    # Agregamos una columna al dataframe con el índice del rubro que lo sacamos del código de rubro presupuestal
    data['Index_Rubro'] = data.apply(lambda x: x['Rubro'].split("-")[3], axis = 1)
    
    # Filtramos el dataframe para que solo contenga los rubros especificados
    data = data[data['Index_Rubro'].str.contains('12|13|14|16|17|20|21|22|23|25', case = False, regex = True)].reset_index(drop = True)
    
    # Agregamos una columna al dataframe con la descripción del programa asociado a el rubro
    data['Descripción Rubro'] = data.apply(lambda x: rubro_names[x['Index_Rubro']], axis = 1)
    
    # Filtramos el dataframe para que no contenga aquellos registros anulados
    data = data.drop(data[data['Estado'] == 'Anulado'].index).reset_index(drop = True)
    data = data.drop(data[data['Estado'] == 'Anulada'].index).reset_index(drop = True)
    
    # Agregamos una columna al dataframe con la dirección
    data['Dirección'] = data['Index_Rubro'].apply(lambda x: find_key(dir_names,x))
    
    # Reemplazamos los caracteres `\xa0` por espacios en la columna `Recurso`
    data['Recurso'] = data['Recurso'].apply(lambda x: str(x).replace('\xa0', ' '))
    
    # Devolvemos el dataframe filtrado
    return data

# Se define un diccionario con las columnas con valores numéricos de tipo texto que se deben convertir para cada tipo de archivo
cols_to_num ={'CDP':['Valor Inicial','Valor Operaciones','Valor Actual','Saldo por Comprometer'],
              'RP':['Valor Inicial', 'Valor Operaciones', 'Valor Actual', 'Saldo por Utilizar'],
              'Oblig':['Valor Inicial', 'Valor Operaciones','Valor Actual.1','Saldo por Utilizar'],
              'OP':['Valor Pesos', 'Valor Moneda', 'Valor Reintegrado Pesos', 'Valor Reintegrado Moneda']
              }

def clean_bases(df1: pd.DataFrame, dffip: pd.DataFrame, tema: str) -> pd.DataFrame:
    """
    Esta función limpia y une dos dataframes de Pandas.

    Args:
        df1: El primer dataframe de Pandas.
        dffip: El segundo dataframe de Pandas de recurso FIP.
        tema: El tema del dataframe {CDP, RP, Oblig, OP}.

    Returns:
        Un dataframe de Pandas con la concatenación de los dos dataframes con las columnas corregidas 
    """
    # Según el tema seleccionamos las columnas a limpiar
    cols = cols_to_num[tema]
    
    # Convertimos las columnas a números.
    cl1 = str_to_float(df1, cols)
    cl2 = str_to_float(dffip, cols)
    
    # Unimos los dos dataframes.
    total = unificar_data(cl1, cl2)
    
    # Si el tema es "OP" o "OP_Reservas", calculamos el valor neto en pesos.
    if tema == 'OP' or tema =='OP_Reservas':
        total['Valor Neto Pesos'] = total.apply(lambda x: x['Valor Pesos']-x['Valor Reintegrado Pesos'], axis = 1)
    
    # Aplicamos la función filter rubros para obtener la dirección y el programa correspondiente
    total = filter_rubros(total)
    
    # Devolvemos el dataframe concatenado, corregido y filtrado
    return total

# Función para limpiar el reporte de ejecución agregada
def clean_general(df: pd.DataFrame, DIP: bool = False) -> pd.DataFrame:
    """
    Esta función toma el reporte de ejecución agregada, lo filtra solo para las direcciones de la subdirección
    y agrupa la información para cada programa

    Args:
        df: El Reporte de ejecución agregada

    Returns:
        El dataframe del reporte de ejecución agregada filtrado y corregido
    """
    
    # Eliminmos las filas que tienen valores faltantes en la columna 0.
    RG = df.dropna(subset = df.columns[0])
    
    # Agregamos una columna al dataframe con el índice del rubro.
    RG['Index_Rubro'] = RG['RUBRO'].apply(lambda x: x.split("-")[-1])
    
    # Obtenemos un diccionario con los nombres de los recursos según el indicativo presupuestal
    rec_names = {
    10:'RECURSOS CORRIENTES',
    11:'OTROS RECURSOS DEL TESORO',
    13:'RECURSOS DEL CREDITO EXTERNO PREVIA AUTORIZACION',
    16:'FONDOS ESPECIALES'
    }

    # Filtramos el dataframe para que solo contenga los rubros especificados
    RG = RG[(RG['Index_Rubro'].str.contains('12|13|14|16|17|20|21|22|23|25', case = False, regex = True)) & (RG['TIPO']=='C')].reset_index(drop = True)
    
    # Agregamos una columna al dataframe con la descripción del rubro
    RG['Descripción Rubro'] = RG.apply(lambda x: rubro_names[x['Index_Rubro']], axis = 1)
    
    # Agregamos una columna al dataframe con la dirección
    RG['Dirección'] = RG['Index_Rubro'].apply(lambda x: find_key(dir_names,x))
    
    # Agregamos una columna al dataframe con el recurso
    RG['Recurso'] = RG['REC'].apply(lambda x: rec_names[int(x)])
    
    #  Agrupamos el dataframe por las columnas `Index_Rubro` y `Recurso` para tener el valor general para cada rubro según su recurso
    RG = RG.groupby(['Index_Rubro','Recurso'], as_index = False).agg({
        'Dirección':'first',            # Tomamos la dirección asociado al rubro
        'Descripción Rubro' : 'first',  # Tomamos el programa asociado al rubro
        'APR. INICIAL' : 'sum',         # Sumamos la apropiación inicial
        'APR. ADICIONADA' : 'sum',      # Sumamos las adiciones a la apropiación por rubro
        'APR. REDUCIDA' : 'sum',        # Sumamos las reducciones a la apropiación por rubro
        'APR. VIGENTE': 'sum',          # Sumamos la apropiación vigente por rubro
        'APR BLOQUEADA': 'sum',         # Sumamos la apropiación bloqueada por rubro
        'APR. DISPONIBLE' : 'sum',      # Sumamos la apropiación disponible por rubro
        'CDP': 'sum',                   # Sumamos el total de CDP por rubro
        'COMPROMISO': 'sum',            # Sumamos los compromisos realizados por rubro
        'OBLIGACION' : 'sum',           # Sumamos las obligaciones por rubro
        'ORDEN PAGO' : 'sum',           # Sumamos las órdenes de pago por rubro
        'PAGOS' : 'sum'                 # Sumamos el total de pagos hechos por rubro
        })   
    
    # En el caso que sea verdadero el caso de la DIP, filtramos por solo aquellos caso en los que la dirección es la de Inclusión Productiva
    if DIP:
        # Filtramos solo aquellos datos que son de la dirección
        RG = RG[RG['Dirección'] == 'Inclusión Productiva'].reset_index(drop = True)
        
        RG['% COMPROMETIDO (B/A)'] = RG.apply(lambda x: round(int(x['COMPROMISO'])/int(x['APR. VIGENTE']),4), axis = 1)
        RG['APR. DISPONIBLE (A-B)'] = RG.apply(lambda x: int(x['APR. VIGENTE']) - int(x['COMPROMISO']), axis = 1)
        RG['% EJECUCIÓN (C/A)'] = RG.apply(lambda x: round(int(x['PAGOS'])/int(x['APR. VIGENTE']),4), axis = 1)
    
        # Seleccionamos las columnas que necesitamos
        RG = RG[['RUBRO','Descripción Rubro','APR. INICIAL','APR. REDUCIDA','APR. VIGENTE','CDP','COMPROMISO',
                 '% COMPROMETIDO (B/A)','APR. DISPONIBLE (A-B)','OBLIGACION','PAGOS','% EJECUCIÓN (C/A)']]
    
        # Renombramos las columnas que necesitamos
        RG = RG.rename(columns={'Descripción Rubro':'DESCRIPCION','APR. VIGENTE':'APR. VIGENTE (A)','COMPROMISO':'COMPROMISO (B)', 'PAGOS':'PAGOS (C)'})

    # Devolvemos el dataframe limpio y agrupado
    return RG
