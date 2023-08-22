'''
- Script main.py
- Script encargado de activar y ejecutar todas las funciones definidas en los demás scripts
- Autor: Wilson Andrés Pinzón (wilson.pinzon@prosperidadsocial.gov.co)
- Fecha_Actualización: 23/08/22
'''

# Importamos las librearias
import pandas as pd
from datetime import datetime

# Importamos las funciones que se han definidos en los demás scripts
from Load_Data import get_data
from Modulo_1 import clean_bases, clean_general
from Modulo_2 import get_pre_second_base, get_pre_re_second_base
from Modulo_3 import get_third_base
from Modulo_4 import get_fourth_base
from Modulo_5 import get_comparativa_vigencias
from export import export_data
from Create_Report import datos_excel, ctr_reservas

# Función para encontrar la fecha
def get_date():
    while True:
        fecha_str = input("Ingrese una fecha (dd/mm/aaaa): ")

        try:
            fecha = datetime.strptime(fecha_str, "%d/%m/%Y")
            break
        except ValueError:
            print("Fecha inválida. Por favor ingrese una fecha en el formato dd/mm/aaaa.")
    
    return fecha


def run_code()-> dict:
    """Función principal donde se van a ejecutar todos los cambios sobre el dataframe
    
    return:
        diccionario donde se almacenan los DataFrame modificados y creados
    """
    
    ## Solicitamos la información del script Get_data, este nos devuelve el diccionario  con los DataFrame y la fecha de cargue
    bases_de_datos, fecha_str = get_data()
    
    ## Creamos el archivo donde se va a guardar todos los resultados
    resultados = dict()
    
    ## Obtenemos los diferentes parámetros desagregados sobre la fecha de actualización
    fecha = datetime.strptime(fecha_str, "%y-%m-%d")
    num_mes = fecha.month
    num_año = fecha.year
    str_fecha = fecha.strftime("%Y/%m/%d")
    
    ## Modulo 1:
    ### Limpieza de Bases Normales
    # Utilizamos un try - except para poder manejar errores y en el caso que hayan mostrar el sitio donde están ocurriendo los errores
    try:
        #Vigencias
        resultados['CDP'] = clean_bases(bases_de_datos['CDP'], bases_de_datos['CDP_FIP'],'CDP')
        resultados['RP'] = clean_bases(bases_de_datos['RP'], bases_de_datos['RP_FIP'], 'RP') 
        resultados['Oblig'] = clean_bases(bases_de_datos['Oblig'], bases_de_datos['Oblig_FIP'], 'Oblig') 
        resultados['OP'] = clean_bases(bases_de_datos['OP'], bases_de_datos['OP_FIP'], 'OP') 
        resultados['RP_Reserva'] = clean_bases(bases_de_datos['RP_Reservas'], bases_de_datos['RP_FIP_Reservas'], 'RP') 
        resultados['Oblig_Reserva'] = clean_bases(bases_de_datos['Oblig_Reservas'],bases_de_datos['Oblig_FIP_Reservas'], 'Oblig') 
        resultados['OP_Reserva'] = clean_bases(bases_de_datos['OP_Reservas'], bases_de_datos['OP_FIP_Reservas'], 'OP') 
        
        #Vigencia Anterior
        resultados['CDP_22'] = clean_bases(bases_de_datos['CDP_22'], bases_de_datos['CDP_FIP_22'], 'CDP') 
        resultados['RP_22'] = clean_bases(bases_de_datos['RP_22'], bases_de_datos['RP_FIP_22'], 'RP') 
        resultados['Oblig_22'] = clean_bases(bases_de_datos['Oblig_22'], bases_de_datos['Oblig_FIP_22'], 'Oblig')    
        resultados['OP_22'] = clean_bases(bases_de_datos['OP_22'], bases_de_datos['OP_FIP_22'], 'OP')
        resultados['RP_Reserva_22'] = clean_bases(bases_de_datos['RP_Reservas_22'],bases_de_datos['RP_FIP_Reservas_22'],'RP')
        resultados['Oblig_Reserva_22'] = clean_bases(bases_de_datos['Oblig_Reservas_22'],bases_de_datos['Oblig_FIP_Reservas_22'],'Oblig')
        resultados['OP_Reserva_22'] = clean_bases(bases_de_datos['OP_Reservas_22'], bases_de_datos['OP_FIP_Reservas_22'], 'OP')
        
        #Vigencia x Anteriores
        resultados['CDP_21'] = clean_bases(bases_de_datos['CDP_21'], bases_de_datos['CDP_FIP_21'], 'CDP') 
        resultados['RP_21'] = clean_bases(bases_de_datos['RP_21'], bases_de_datos['RP_FIP_21'], 'RP') 
        resultados['Oblig_21'] = clean_bases(bases_de_datos['Oblig_21'], bases_de_datos['Oblig_FIP_21'], 'Oblig')    
        resultados['OP_21'] = clean_bases(bases_de_datos['OP_21'], bases_de_datos['OP_FIP_21'], 'OP')
        resultados['RP_Reserva_21'] = clean_bases(bases_de_datos['RP_Reservas_21'],bases_de_datos['RP_FIP_Reservas_21'],'RP')
        resultados['Oblig_Reserva_21'] = clean_bases(bases_de_datos['Oblig_Reservas_21'],bases_de_datos['Oblig_FIP_Reservas_21'],'Oblig')
        resultados['OP_Reserva_21'] = clean_bases(bases_de_datos['OP_Reservas_21'], bases_de_datos['OP_FIP_Reservas_21'], 'OP')
        
    # Manejo de errores
    except:
        print('Problemas en la sección 1')
        raise

    ### Limpieza de Reportes Generales
    try:
        resultados['RG'] = clean_general(bases_de_datos['Ejecución_Presupuestal_Agregada'])
        resultados['RG22'] = clean_general(bases_de_datos['Ejecución_Presupuestal_Agregada_22'])
        resultados['RG21'] = clean_general(bases_de_datos['Ejecución_Presupuestal_Agregada_21'])
        
    except:
        print("Problemas con los reportes generales")
        raise
    
    ### Creamos los DataFrame que van a ser usados en el reporte financiero de excel
    try:
        resultados['RG_Excel'] = clean_general(bases_de_datos['Ejecución_Presupuestal_Agregada'], DIP = True)
        resultados['RG_Excel'] = datos_excel(resultados['RG_Excel'])
    except:
        print('Problemas con la creación de los archivos excel')
        raise
    
    ## Modulo 2
    # Creamos los reportes desagregados de forma mensual para cada programa de la subdirección, se crean para la vigencia como para las demás vigenvias con tal de crear los documentos comparativos
    try:
        resultados['Base_Rubros'] = get_pre_second_base(resultados['RG'], resultados['CDP'], resultados['RP'], resultados['Oblig'], 
                                                                      resultados['OP'], num_mes)
    
        resultados['Base_Rubros_22'] = get_pre_second_base(resultados['RG22'], resultados['CDP_22'], resultados['RP_22'], resultados['Oblig_22'], 
                                                                      resultados['OP_22'], 12)
        
        resultados['Base_Rubros_21'] = get_pre_second_base(resultados['RG21'], resultados['CDP_21'], resultados['RP_21'], resultados['Oblig_21'], 
                                                                      resultados['OP_21'], 12)
        
        resultados['Base_Rubros_Reservas']= get_pre_re_second_base(resultados['RP_Reserva'],resultados['Oblig_Reserva'],resultados['OP_Reserva'], 
                                                                   num_mes)
        
        resultados['Base_Rubros_Reservas_22']= get_pre_re_second_base(resultados['RP_Reserva_22'],resultados['Oblig_Reserva_22'],resultados['OP_Reserva_22'],
                                                                      12)

        resultados['Base_Rubros_Reservas_21']= get_pre_re_second_base(resultados['RP_Reserva_21'],resultados['Oblig_Reserva_21'],resultados['OP_Reserva_21'],
                                                                      12)

    
    ## Creación Base Comparativa
        resultados['Base_Comparativa'] = get_comparativa_vigencias(resultados['Base_Rubros_21'], resultados['Base_Rubros_22'], resultados['Base_Rubros'], num_año)
        resultados['Base_Comparativa_Res'] = get_comparativa_vigencias(resultados['Base_Rubros_Reservas_21'], resultados['Base_Rubros_Reservas_22'], resultados['Base_Rubros_Reservas'], num_año)
    
    except:
        print("Problemas en el módulo 2")
        raise
    ## Aplicación del módulo 3
    try:
        resultados['Base_Compromisos'] = get_third_base(resultados['RP'], resultados['Oblig'], resultados['OP'])
        resultados['Base_Compromisos_Reservas'] = get_third_base(resultados['RP_Reserva'], resultados['Oblig_Reserva'], resultados['OP_Reserva'])
        resultados['Reservas_Excel'] = ctr_reservas(resultados['Base_Compromisos_Reservas'])
    except:
        print("Problemas en la sección 3")
        raise
    
    # Aplicación del módulo 4
    try:
        resultados['BASE_RP_OP'] = get_fourth_base(resultados['RP'], resultados['OP'], num_mes)
    except:
        print("Problemas en la sección 4")
        raise
    
    # Guardamos la información de la fecha de corte en un dataframe para ser exportado y leído posteriormente en Power BI
    resultados['dates'] = pd.DataFrame({'Fecha':[fecha.strftime("%Y-%m-%d")]})
    
    # Devolvemos el diccionario con los DataFrames creados
    return resultados


# Función principal que corre el programa
if __name__ == '__main__':
    # Se guarda en resultados el diccionario con los dataframes modificados
    resultados = run_code()
    
    # Se exportan los datos con la función export_data del script export con el diccionario resultados.
    export_data(resultados)
