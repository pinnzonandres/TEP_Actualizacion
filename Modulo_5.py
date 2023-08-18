# Cargamos los modulos necesarios
import pandas as pd

# Función para concatenar la información comparativa de vigencias según el año actual
def get_comparativa_vigencias(base_x_anteriores: pd.DataFrame, base_anterior: pd.DataFrame, base_vigencia: pd.DataFrame, año: int) -> pd.DataFrame:
    """
    Esta función concatena la información comparativa de vigencias según el año actual.

    Args:
    base_x_anteriores: El dataframe con los datos de vigencias anteriores.
    base_anterior: El dataframe con los datos de la vigencia anterior.
    base_vigencia: El dataframe con los datos de la vigencia actual.
    año: El año actual.

    Returns:
    El dataframe con los datos de las tres vigencias, concatenadas.
    """
    
    # Definimos una columna que indique el año correspondiente a la vigencia de cada dataframe
    base_x_anteriores['Vigencia'] = int(año) - 2
    base_anterior['Vigencia'] = int(año) - 1
    base_vigencia['Vigencia'] = int(año)
    
    # Concatenamos los tres dataframes
    result = pd.concat([base_x_anteriores, base_anterior, base_vigencia], ignore_index = True)
    
    # Devolvemos el dataframe concatenado
    return result
