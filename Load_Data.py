# Importación de Librerias
import os
import pandas as pd

# Definición de parámetros base

## Se crea un diccionario con la estructura de los archivos que se van a leer de la vigencia actual
base_nuevos = {
    'CDP': {'file' : '1 CDP', 'header' : 0},
    'CDP_FIP' : {'file' : '5 CDP', 'header' : 0},
    'RP' : {'file' : '2 RP', 'header' : 0},
    'RP_FIP' : {'file' : '6 RP', 'header' : 0},
    'Oblig' : {'file' : '3 Oblig', 'header' : 0},
    'Oblig_FIP' : {'file' : '7 Oblig','header' : 0},
    'OP': {'file' : '4 OP', 'header' : 0},
    'OP_FIP': {'file' : '8 OP', 'header' : 0},
    'Ejecución_Presupuestal_Agregada': {'file' : 'EjecucionPresupuestalAgregada', 'header' : 3},
    'Oblig_Reservas': {'file' : '3.1 Oblig', 'header' : 0},
    'Oblig_FIP_Reservas': {'file' : '7.1 Oblig', 'header': 0},
    'OP_Reservas': {'file' : '4.1 OP', 'header' : 0},
    'OP_FIP_Reservas': {'file' : '8.1 OP', 'header' : 0},
}

## Diccionario con la estructura de los archivos que se van a leer de las reservas de la vigencia
base_reservas = {
    'RP_Reservas': {'file' : '2.1 RP', 'header': 0},
    'RP_FIP_Reservas': {'file' : '6.1 RP', 'header': 0},
}

## Diccionario con la estructura base de los archivos de la vigencia anterior
base_2022 = {
    'CDP_22': {'file' : '1 CDP', 'header' : 0},
    'CDP_FIP_22' : {'file' : '5 CDP', 'header' : 0},
    'RP_22' : {'file' : '2 RP', 'header' : 0},
    'RP_FIP_22' : {'file' : '6 RP', 'header' : 0},
    'Oblig_22' : {'file' : '3 Oblig', 'header' : 0},
    'Oblig_FIP_22' : {'file' : '7 Oblig','header' : 0},
    'OP_22': {'file' : '4 OP', 'header' : 0},
    'OP_FIP_22': {'file' : '8 OP', 'header' : 0},
    'Ejecución_Presupuestal_Agregada_22': {'file' : 'EjecucionPresupuestalAgregada', 'header' : 3},
    'RP_Reservas_22': {'file' : '2.1 RP', 'header': 0},
    'RP_FIP_Reservas_22': {'file' : '6.1 RP', 'header': 0},
    'Oblig_Reservas_22': {'file' : '3.1 Oblig', 'header' : 0},
    'Oblig_FIP_Reservas_22': {'file' : '7.1 Oblig', 'header': 0},
    'OP_Reservas_22': {'file' : '4.1 OP', 'header' : 0},
    'OP_FIP_Reservas_22': {'file' : '8.1 OP', 'header' : 0}
}

## Diccionario con la estrucuta de los archivos que de la vigencia referente a los dos años anteriores a la vigencia actual
base_2021 = {
    'CDP_21': {'file' : '1 CDP', 'header' : 0},
    'CDP_FIP_21' : {'file' : '5 CDP', 'header' : 0},
    'RP_21' : {'file' : '2 RP', 'header' : 0},
    'RP_FIP_21' : {'file' : '6 RP', 'header' : 0},
    'Oblig_21' : {'file' : '3 Oblig', 'header' : 0},
    'Oblig_FIP_21' : {'file' : '7 Oblig','header' : 0},
    'OP_21': {'file' : '4 OP', 'header' : 0},
    'OP_FIP_21': {'file' : '8 OP', 'header' : 0},
    'Ejecución_Presupuestal_Agregada_21': {'file' : 'EjecucionPresupuestalAgregada', 'header' : 3},
    'RP_Reservas_21': {'file' : '2.1 RP', 'header': 0},
    'RP_FIP_Reservas_21': {'file' : '6.1 RP', 'header': 0},
    'Oblig_Reservas_21': {'file' : '3.1 Oblig', 'header' : 0},
    'Oblig_FIP_Reservas_21': {'file' : '7.1 Oblig', 'header': 0},
    'OP_Reservas_21': {'file' : '4.1 OP', 'header' : 0},
    'OP_FIP_Reservas_21': {'file' : '8.1 OP', 'header' : 0}
}
 
## Se define un diccionario donde se van a guardar los archivos que van a ser cargados a Python
'''
En la estructura del diccionario Database se deja cómo entrada base el parámetro None para poder asegurar que entran los archivos necesarios
'''
database = {
    'CDP': None,
    'CDP_FIP' : None ,
    'RP' : None ,
    'RP_FIP' : None ,
    'Oblig' : None ,
    'Oblig_FIP' : None ,
    'OP': None ,
    'OP_FIP': None ,
    'Ejecución_Presupuestal_Agregada': None,
    'Oblig_Reservas': None,
    'Oblig_FIP_Reservas': None,
    'OP_Reservas': None,
    'OP_FIP_Reservas': None,
    'RP_Reservas': None,
    'RP_FIP_Reservas': None,
    'CDP_22': None,
    'CDP_FIP_22' : None,
    'RP_22' : None,
    'RP_FIP_22' : None,
    'Oblig_22' : None,
    'Oblig_FIP_22' : None,
    'OP_22': None,
    'OP_FIP_22': None,
    'Ejecución_Presupuestal_Agregada_22': None,
    'RP_Reservas_22':None,
    'RP_FIP_Reservas_22':None,
    'Oblig_Reservas_22': None,
    'Oblig_FIP_Reservas_22': None,
    'OP_Reservas_22': None,
    'OP_FIP_Reservas_22': None,
    'CDP_21': None,
    'CDP_FIP_21' : None,
    'RP_21' : None,
    'RP_FIP_21' : None,
    'Oblig_21' : None,
    'Oblig_FIP_21' :None,
    'OP_21': None,
    'OP_FIP_21': None,
    'Ejecución_Presupuestal_Agregada_21': None,
    'RP_Reservas_21': None,
    'RP_FIP_Reservas_21': None,
    'Oblig_Reservas_21': None,
    'Oblig_FIP_Reservas_21': None,
    'OP_Reservas_21': None,
    'OP_FIP_Reservas_21': None,
}

# Función para la carga de los datos
def get_data() -> tuple[dict, str]:
    """
      Esta función carga los datos de las carpetas `Reportes SIIF Vigencia`, `Reservas Vigencia`, `Base Vigencia Anterior` y `Base Vig x Anteriores`.

        Returns:
            Un tupla con dos elementos:
            * El primer elemento es un diccionario que contiene todos los dataframes cargados de la vigencia actual.
            * El segundo elemento es la fecha de corte de los datos.
    """
    
    # Se obtiene la dirección de la ubicación del Script
    script_dir = os.path.dirname(__file__)
    
    # Se ubica la carpeta donde se encuentran los reportes de la vigencia y se lee la dirección de los archivos excel que están dentro de esta carpeta
    ruta_vigencia = os.path.join(script_dir, '..', 'Archivos Base', 'Reportes SIIF Vigencia')
    
    # Se ubica la carpeta con la fecha más recienta para que cargue los archivos de esta carpeta
    ruta_reciente_vigencia = os.path.join(ruta_vigencia,sorted(os.listdir(ruta_vigencia))[-1])
    print("Se están cargando los archivos de la carpeta,", ruta_reciente_vigencia)
    
    # Se guarda en una lista los nombres de los archivos de tipo excel que están en la carpeta
    archivos_excel_nuevos = [f for f in os.listdir(ruta_reciente_vigencia) if f.endswith(".xlsx")]
    
    # Se toma la fecha de nombre que tiene esta carpeta para utilizar esta fecha más adelante ya que esta es la fecha de corte de los archivos
    fecha_str = ruta_reciente_vigencia.split('\\')[-1]

    # Dirección del ultimo reporte de reservas y se guarda en una lista el nombre de los archivos excel
    ruta_rev= os.path.join(script_dir, '..', 'Archivos Base', 'Reservas Vigencia')
    ruta_reciente_reservas = os.path.join(ruta_rev,sorted(os.listdir(ruta_rev))[-1])
    archivos_excel_rev = [f for f in os.listdir(ruta_reciente_reservas) if f.endswith(".xlsx")]

    # Dirección de la carpeta donde están ubicados los archivos de la vigencia anterior
    ruta_2022 = os.path.join(script_dir, '..', 'Archivos Base', 'Base Vigencia Anterior')
    archivos_excel_2022 = [f for f in os.listdir(ruta_2022) if f.endswith(".xlsx")]
    
    # Dirección de la carpeta donde están ubicados los archivos referentes a las dos vigencias anteriores a la vigencia actual
    ruta_2021 = os.path.join(script_dir, '..', 'Archivos Base', 'Base Vig x Anteriores')
    archivos_2021 = [f for f in os.listdir(ruta_2021) if f.endswith(".xlsx")]
    
    # Se crea un diccionario para establecer la ruta y los parámetros definidos anteriormente para la carga correcta de cada archivo
    # Archivos de la vigencia
    data_nuevos = {i:{'file': os.path.join(ruta_reciente_vigencia, [n for n in archivos_excel_nuevos if base_nuevos[i]['file'] in n][-1]), 'header':base_nuevos[i]['header'] } for i in base_nuevos.keys()}
    
    # Archivos de la reserva de la vigencia
    data_rev = {i: {'file': os.path.join(ruta_reciente_reservas, [n for n in archivos_excel_rev if base_reservas[i]['file'] in n][-1]),'header':base_reservas[i]['header']} for i in base_reservas.keys()}
    
    # Archivos de la vigencia anterior
    data_2022 = {i: {'file': os.path.join(ruta_2022, [n for n in archivos_excel_2022 if base_2022[i]['file'] in n][-1]), 'header': base_2022[i]['header']} for i in base_2022.keys()}
    
    # Archivos de la vigencia referente a los dos años anteriores
    data_2021 = {i: {'file': os.path.join(ruta_2021, [n for n in archivos_2021 if base_2021[i]['file'] in n][-1]), 'header': base_2021[i]['header']} for i in base_2021.keys()}    
    
    # Se almacena en una lista los diccionarios con los parámetros de carga establecidos anteriormente para hacer un loop que pueda cargar toda la información
    datos = [data_nuevos, data_rev, data_2022, data_2021]

    # Se ejecuta un loop que sobre cada diccionario que permita cargar los archivos a nuestro diccionario database
    for folder in datos:
        for i in folder.keys():
            # En el loop hacemos un try except para veríficar que la información se está guardando de forma correcta, en el caso que no es así se le pide que nos indice
            # cuál es la carpeta que está generando problemas con el cargue de la información
            try:
                # Se lee y se guarda la información del archivo excel con la ruta y parámetros establecidos en el diccionario
                database[i] = pd.read_excel(folder[i]['file'], header = folder[i]['header'])
            except:
                # Se indica el lugar donde hay un problema de cargue.
                print("Problema en la carpeta", str(folder))
                print("No se pudo cargar la base,",i)
                raise
        
    # La función devuelve el archivo database donde se encuentran todos los dataframes con la información necesaria y la fecha de corte de la actualización del tablero
    return database, fecha_str
    
    
    
    


