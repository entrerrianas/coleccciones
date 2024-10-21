import pandas as pd
def sacar_acento(letra):
    """
    Función para devolver una letra sin acentro si lo tiene
    """
    letras_con_acento = {'Á':'A', 'É':'E', 'Í':'I', 'Ó':'O', 'Ú':'U'}
    return letra if letra not in letras_con_acento else letras_con_acento[letra]


def convertir_string(df, columna):
    '''como en la clumna que tiene texto hay una que es u número
    en algunos casos tira error al ordenar'''
    df[columna] = df[columna].astype(str)

    return df

def borrar_nan(df):
    df['Ciudad'] = df['Ciudad'].apply(str)
    return df

def mod_vinos(df):
    df = borrar_nan(df)
    df = convertir_string(df, 'Denominación')
    return df

def convertir_fechas(df):
    df.rename(columns={'Feha inicio': 'Fecha inicio'}, inplace=True)
    df['Fecha inicio'] = pd.to_datetime(df['Fecha inicio'])
    df['Fecha final'] = pd.to_datetime(df['Fecha final'])
    return df
    
def generar_rutas(df):
    df_sin_nan = df.copy()
    df_sin_nan = df_sin_nan.dropna(subset=['Rutas'])
    df_sin_nan['cat_sep'] = df_sin_nan['Rutas'].str.split('; ')
    lista_rutas = [item for sublist in df_sin_nan['cat_sep'].tolist() for item in sublist]
    rutas_unicas = sorted(set(lista_rutas))
    return rutas_unicas
