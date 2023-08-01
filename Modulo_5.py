import pandas as pd

def get_comparativa_vigencias(base_x_anteriores, base_anterior, base_vigencia, año):
    base_x_anteriores['Vigencia'] = int(año) - 2
    base_anterior['Vigencia'] = int(año) - 1
    base_vigencia['Vigencia'] = int(año)
    
    result = pd.concat([base_x_anteriores, base_anterior, base_vigencia], ignore_index = True)
    
    return result
