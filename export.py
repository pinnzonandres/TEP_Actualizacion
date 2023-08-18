# Importamos las librerias necesarias
import pandas as pd
import os

# Importamos la función export_report que se encuentra en el Script Create_Report
from Create_Report import export_report

# Definimos una función que permita ubicar las direcciones de las carpetas donde se va a guardar la información
def set_path(nombre_folder: str) -> tuple[str, str, str]:
    """
    Esta función permite ubicar las direcciones de las carpetas donde se va a guardar la información.

    Args:
    nombre_folder: El nombre de la carpeta.

    Returns:
    Una tupla con las rutas de las tres carpetas creadas.
    """
    # Obtenemos la ruta del script actual
    script_dir = os.path.dirname(__file__)
    
    # Ubicamos la carpeta `Resultados`
    folderpath = os.path.join(script_dir, '..', 'Resultados')
    
    # Creamos la ruta de la dirección de la carpeta resultados con la nueva carpeta con el argumento nombre_folder
    nueva_carpeta_path = os.path.join(folderpath, nombre_folder)
    
    # Creamos la carpeta anterior
    os.mkdir(nueva_carpeta_path)
    
    # Crea las tres subcarpetas dentro de la nueva carpeta
    # La carpeta que tiene el archivo base para el tablero de Power BI
    base_tablero_path = os.path.join(nueva_carpeta_path, "Base_Tablero")
    os.mkdir(base_tablero_path)
    
    # La carpeta que va a tener la información modificada en formato crudo
    archivos_modificados_path = os.path.join(nueva_carpeta_path, "Archivos_Modificados")
    os.mkdir(archivos_modificados_path)
    
    # La carpeta que va a tener el archivo excel que automatiza el reporte excel 
    archivos_formato_excel_path = os.path.join(nueva_carpeta_path, "Reporte_Excel")
    os.mkdir(archivos_formato_excel_path)
    
    # Devolvemos la tupla de rutas creadas para poder guardar información en archivos excel
    return base_tablero_path, archivos_modificados_path, archivos_formato_excel_path


# Función para exportar los dataframe en archivos excel
def export_data(bases_de_datos: pd.DataFrame) -> None:
    """
    Esta función exporta los datos de los `bases_de_datos` a archivos Excel.

    Args:
    bases_de_datos: El dataframe con los datos.
    """
    # Creamos y cargamos las rutas de las carpetas creadas en la función set_path
    path1, path2, path3 = set_path(bases_de_datos['dates']['Fecha'].values[0])
    
    # Definimos las listas de dataframes que van a ser exportados en cada carpeta o archivo
    bases = ['CDP', 'RP', 'Oblig', 
             'OP', 'RP_Reserva', 
             'Oblig_Reserva', 'OP_Reserva', 
             'Base_Compromisos',
             'Base_Compromisos_Reservas', 
             'BASE_RP_OP', 'RG', 'Base_Rubros','Base_Comparativa','Base_Comparativa_Res']
    
    nombres = ['1_CDP', '2_RP', '3_Oblig', 
             '4_OP', '2.1_RP_Reservas', 
             '3.1_Oblig_Reservas', '4.1_OP_Reservas', 
             '7_Base_Compromisos',
             '7.1_Base_Compromisos_Reservas', 
             '8_BASE_RP_OP', '5_Reporte General', '6_Base_Rubros',
             '9_Base_Comparativa_Ejecución',
             '10_Base_Comparativa_Reservas']

    bases_tablero = ['dates','RG','Base_Rubros','Base_Compromisos',
                     'Base_Compromisos_Reservas','BASE_RP_OP',
                     'Base_Comparativa','Base_Comparativa_Res']
    
    nombres_tablero = ['Fecha_Tablero','1_Reporte_General','2_Balance Proyectos',
                       '3_Base Compromisos','3.1_Base_Compromisis_Reservas','4_Base_RP_OP',
                       '5_Base_Comparativa','6_Base Comparativa Reservas']
    
    # Exportamos cada base de datos a un archivo Excel
    for pair in zip(bases, nombres):
        try:
            path_f = os.path.join(path2,pair[1])
            bases_de_datos[pair[0]].to_excel(path_f+'.xlsx', index = False, sheet_name =pair[1])
        except:
            print('No se logró exportar la base: ', pair[1])

    # Exportamos la base de datos `bases_tablero` a un archivo Excel 
    path_to_base = os.path.join(path1,'Base_Tablero_Ejecución Presupuestal'+'.xlsx')
    writer = pd.ExcelWriter(path_to_base, engine='xlsxwriter')
    for pair in zip(bases_tablero,nombres_tablero):
        bases_de_datos[pair[0]].to_excel(writer, sheet_name= pair[1], index= False)
    writer.close()
    
    # Exportamos la base para el tablero en la carpeta donde se encuentra la información del tablero
    path_to_base_2 = os.path.join('..\\Tablero\\','Base_Tablero_Ejecución Presupuestal'+'.xlsx')
    writer = pd.ExcelWriter(path_to_base_2, engine='xlsxwriter')
    for pair in zip(bases_tablero,nombres_tablero):
        bases_de_datos[pair[0]].to_excel(writer, sheet_name= pair[1], index= False)
    writer.close()
    
    # Creamos y exportaos el reporte excel por medio de la función export report 
    export_report(bases_de_datos, path3, pd.to_datetime(bases_de_datos['dates']['Fecha'].values[0]).month, pd.to_datetime(bases_de_datos['dates']['Fecha'].values[0]).year)