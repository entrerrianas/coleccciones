import pandas as pd


# Cargar el archivo CSV
def cargar_archivo(data):
    archivo_csv = data
    df = pd.read_csv(archivo_csv)
    
    return df

def borrar_nan(df):
    df['Ciudad'] = df['Ciudad'].apply(str)
    return df


