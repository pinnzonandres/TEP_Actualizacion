'''
- Script Modulo_4.py
- Script encargado de realizar un reporte que reporta los giros realizados a cada compromiso por cada mes de la vigencia.
- Autor: Wilson Andrés Pinzón (wilson.pinzon@prosperidadsocial.gov.co)
- Fecha_Actualización: 23/08/22
'''

# Cargamos las librerias necesarias
import pandas as pd
# Cargamos una función del script modulo_2 que añade la columna de mes
from Modulo_2 import _month_add

# Se definen los parámetros iniciales necesarios para el trabajo de la función
# Lista de Meses
month_list = ['Enero','Febrero','Marzo', 
              'Abril','Mayo','Junio', 
              'Julio','Agosto','Septiembre',
              'Octubre','Noviembre','Diciembre']

# Diccionario que asocia el número del mes según el nombre del mes
dict_month = {'Enero':1,'Febrero':2,'Marzo':3, 
              'Abril':4,'Mayo':5,'Junio':6, 
              'Julio':7,'Agosto':8,'Septiembre':9,
              'Octubre':10,'Noviembre':11,'Diciembre':12}

def get_fourth_base(RP: pd.DataFrame, OP: pd.DataFrame, month: int)-> pd.DataFrame:
    """
    Esta función obtiene el dataframe el análisis mensual de giros y obligaciones por RP

    Args:
    RP: El dataframe de compromisos
    OP: El dataframe de órdenes de pago.
    month: El mes hasta donde se va a realizar el dataframe

    Returns:
    El dataframe base para el cuarto nivel de análisis.
    """
    # Filtramos las ordenes de pago solo por aquellas que ya están pagadas  
    OP = OP[OP['Estado']=='Pagada'].reset_index(drop = True)
    
    # Agrupamos el dataframe de RPs por el compromiso, índice de rubro y recurso.
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
    
    ## Añadimos el mes a la base GRP
    GRP = _month_add(GRP, 'Fecha de Creacion')

    ## Añadimos la columna de Tipo de Contratista
    GRP['Tipo Contratista'] = GRP['Tipo Identificacion'].apply(lambda x: 'Persona natural' if x =='Cédula de Ciudadanía' else 'Persona jurídica')
    
    ## Añadimos las columnas de mes a la base OP
    MOP = _month_add(OP, 'Fecha de pago')
    
    # Agrupamos la base MOP por las columnas necesarias para el merge
    GOP = MOP.groupby(by = ['Compromisos','Index_Rubro','No. Mes','Recurso'], as_index = False).agg({
        'Fecha de Registro':'first',
        'Fecha de pago':'first',
        'Valor Neto Pesos':'sum',
        'Mes':'first'
        })
    
    # Renombramos la columna Valor neto pesos como el valor de las órdenes de pago
    GOP = GOP.rename(columns = {'Valor Neto Pesos' : 'Valor Ordenes de Pago'})
      
    # Creamos un diccionario para guardar los compromisos y los rubros
    Comp_Rubro ={i:list(set(list(set(GRP[GRP['Compromisos']==i]['Index_Rubro'].values)))) for i in list(set(GRP['Compromisos'].values))}
    
    # Creamos un dataframe vacío
    result = pd.DataFrame()
    
    # Guardamos la información de los RP agrupados en el dataframe vacio
    result = pd.concat([result, GRP], ignore_index = True)
    
    # Por cada compromiso y rubro, agregamos los meses faltantes según la fecha de registro del compromiso
    for i in Comp_Rubro:
        for j in Comp_Rubro[i]:
            # Creamos un dataframe que guarde la información del compromiso según su rubro presupuestal
            df = GRP[(GRP['Compromisos']== i) & (GRP['Index_Rubro']== j)]
            
            # Definimos la lista como los meses que han transcurrido durante la vigencia
            faltantes = month_list[df['No. Mes'][df.index[0]]:month]
            
            # Creamos un dataframe en el que guarda la información del compromiso en sobre cada mes transcurrido en la vigencia
            for n in faltantes:
                data = df
                
                # Guardamos el número del mes 
                data.loc[data.index,'No. Mes'] = dict_month[n]
                
                # Guardamos el mes correspondiente
                data.loc[data.index,'Mes'] = n
                
                # Añadimos la información creada en el dataframe vacío
                result = pd.concat([result, data], ignore_index = True)
                
    # Unimos el resultado del dataframe de compromisos por mes con los giros realizados en cada mes
    GR = result.merge(GOP, how = 'left', on = ['Compromisos', 'Index_Rubro','No. Mes','Mes','Recurso'])
    
    # Reemplazamos los valores nulos por 0 para evitar inconvenientes en la lectura de los datos
    GR['Valor Ordenes de Pago'].fillna(0, inplace = True)
    
    # Organizamos el dataframe resultante por los meses
    GR = GR.sort_values('No. Mes' , ascending = True, ignore_index = True)
    
    # Creamos la columna Valor neto acumulado que hace la suma de los giros realizados mensualmente para cada compromiso
    GR['Valor Neto Acumulado'] = GR.groupby(by =['Compromisos','Index_Rubro','Recurso'])['Valor Ordenes de Pago'].cumsum()
    
    # Devolvemos el dataframe resultante
    return GR