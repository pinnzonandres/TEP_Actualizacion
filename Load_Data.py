# Se importan las librerías necesarias para el funcionamiento del código
import os
import pandas as pd

# Se define un diccionario que mapea cada archivo a sus correspondientes bases de datos
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

base_reservas = {
    'RP_Reservas': {'file' : '2.1 RP', 'header': 0},
    'RP_FIP_Reservas': {'file' : '6.1 RP', 'header': 0},
}

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

# Se define una función para cargar los datos
def get_data():
    # Dirección del archivo
    script_dir = os.path.dirname(__file__)
    
    # Carga de los reportes SIIF de la vigencia
    ruta_vigencia = os.path.join(script_dir, '..', 'Archivos Base', 'Reportes SIIF Vigencia')
    ruta_reciente_vigencia = os.path.join(ruta_vigencia,sorted(os.listdir(ruta_vigencia))[-1])
    print("Se están cargando los archivos de la carpeta,", ruta_reciente_vigencia)
    archivos_excel_nuevos = [f for f in os.listdir(ruta_reciente_vigencia) if f.endswith(".xlsx")]
    
    fecha_str = ruta_reciente_vigencia.split('\\')[-1]

    # Dirección del ultimo reporte de reservas
    ruta_rev= os.path.join(script_dir, '..', 'Archivos Base', 'Reservas Vigencia')
    ruta_reciente_reservas = os.path.join(ruta_rev,sorted(os.listdir(ruta_rev))[-1])
    archivos_excel_rev = [f for f in os.listdir(ruta_reciente_reservas) if f.endswith(".xlsx")]

    ruta_2022 = os.path.join(script_dir, '..', 'Archivos Base', 'Base Vigencia Anterior')
    archivos_excel_2022 = [f for f in os.listdir(ruta_2022) if f.endswith(".xlsx")]
    
    ruta_2021 = os.path.join(script_dir, '..', 'Archivos Base', 'Base Vig x Anteriores')
    archivos_2021 = [f for f in os.listdir(ruta_2021) if f.endswith(".xlsx")]
    
    data_nuevos = {i:{'file': os.path.join(ruta_reciente_vigencia, [n for n in archivos_excel_nuevos if base_nuevos[i]['file'] in n][-1]), 'header':base_nuevos[i]['header'] } for i in base_nuevos.keys()}              
    data_rev = {i: {'file': os.path.join(ruta_reciente_reservas, [n for n in archivos_excel_rev if base_reservas[i]['file'] in n][-1]),'header':base_reservas[i]['header']} for i in base_reservas.keys()}    
    data_2022 = {i: {'file': os.path.join(ruta_2022, [n for n in archivos_excel_2022 if base_2022[i]['file'] in n][-1]), 'header': base_2022[i]['header']} for i in base_2022.keys()}    

    data_2021 = {i: {'file': os.path.join(ruta_2021, [n for n in archivos_2021 if base_2021[i]['file'] in n][-1]), 'header': base_2021[i]['header']} for i in base_2021.keys()}    
    
    datos = [data_nuevos, data_rev, data_2022, data_2021]

    for folder in datos:
        for i in folder.keys():
            try:
                database[i] = pd.read_excel(folder[i]['file'], header = folder[i]['header'])
            except:
                print("Problema en la carpeta", str(folder))
                print("No se pudo cargar la base,",i)
                raise
        
        
    return database, fecha_str
    
    
    
    


