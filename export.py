import pandas as pd
import os
from Create_Report import export_report

def set_path(nombre_folder):
    script_dir = os.path.dirname(__file__)
    folderpath = os.path.join(script_dir, '..', 'Resultados')
    nueva_carpeta_path = os.path.join(folderpath, nombre_folder)
    os.mkdir(nueva_carpeta_path)
    
    # Crea las tres subcarpetas dentro de la nueva carpeta
    base_tablero_path = os.path.join(nueva_carpeta_path, "Base_Tablero")
    os.mkdir(base_tablero_path)
    
    archivos_modificados_path = os.path.join(nueva_carpeta_path, "Archivos_Modificados")
    os.mkdir(archivos_modificados_path)
    
    archivos_formato_excel_path = os.path.join(nueva_carpeta_path, "Reporte_Excel")
    os.mkdir(archivos_formato_excel_path)
    
    return base_tablero_path, archivos_modificados_path, archivos_formato_excel_path



def export_data(bases_de_datos):
    path1, path2, path3 = set_path(bases_de_datos['dates']['Fecha'].values[0])
    
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
             '8_BASE_RP_OP', '5_Reporte General', '6_Base_Rubros','9_Base_Comparativa_Ejecución','10_Base_Comparativa_Reservas']

    bases_tablero = ['dates','RG','Base_Rubros','Base_Compromisos',
             'Base_Compromisos_Reservas','BASE_RP_OP','Base_Comparativa','Base_Comparativa_Res']
    nombres_tablero = ['Fecha_Tablero','1_Reporte_General','2_Balance Proyectos','3_Base Compromisos','3.1_Base_Compromisis_Reservas','4_Base_RP_OP',
                       '5_Base_Comparativa','6_Base Comparativa Reservas']
    
    for pair in zip(bases, nombres):
        try:
            path_f = os.path.join(path2,pair[1])
            bases_de_datos[pair[0]].to_excel(path_f+'.xlsx', index = False, sheet_name =pair[1])
        except:
            print('No se logró exportar la base: ', pair[1])

    path_to_base = os.path.join(path1,'Base_Tablero_Ejecución Presupuestal'+'.xlsx')
    writer = pd.ExcelWriter(path_to_base, engine='xlsxwriter')
    for pair in zip(bases_tablero,nombres_tablero):
        bases_de_datos[pair[0]].to_excel(writer, sheet_name= pair[1], index= False)
    writer.close()
    
    path_to_base_2 = os.path.join('..\\Tablero\\','Base_Tablero_Ejecución Presupuestal'+'.xlsx')
    writer = pd.ExcelWriter(path_to_base_2, engine='xlsxwriter')
    for pair in zip(bases_tablero,nombres_tablero):
        bases_de_datos[pair[0]].to_excel(writer, sheet_name= pair[1], index= False)
    writer.close()
    
    export_report(bases_de_datos, path3, pd.to_datetime(bases_de_datos['dates']['Fecha'].values[0]).month, pd.to_datetime(bases_de_datos['dates']['Fecha'].values[0]).year)