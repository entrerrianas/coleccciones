import streamlit as st
import pandas as pd
import plotly.express as px
import scripts.leer_data as sleer 
import scripts.modificaciones as modi

# Cargar el archivo CSV
archivo_csv = 'files/gins.csv'

df = sleer.cargar_archivo(archivo_csv)
# Título de la aplicación
st.title('Explorador de Datos')
cols_mostrar = ['Título', 'Cosecha', 'Ciudad', 'Provincia', 'Variedad']

tab1, tab2 = st.tabs(["Información general", "Detalles"])

with tab1:
    options = list(df.columns)
    
    # Selector de columnas
    columnas_seleccionadas = st.multiselect('Selecciona las columnas', options)
   # Filtrar por columnas seleccionadas
    if columnas_seleccionadas:
        df_filtrado = df[columnas_seleccionadas]
    else:
        df_filtrado = df

    # Mostrar los datos filtrados
    st.dataframe(df_filtrado)


with tab2:
    
    default_index = options.index('Denominación')
    
    # Crear una lista desplegable para seleccionar la columna
    columna_elegida = st.selectbox('Selecciona una columna:', df.columns, key='columna', index=default_index)

    # Obtener los valores únicos de la columna seleccionada
    valores_columna = sorted(df[columna_elegida].unique())
     # Crear una lista desplegable para seleccionar los valores
    valores_seleccionados = st.multiselect(f'Selecciona valores de {columna_elegida}:', valores_columna)

    # Filtrar el DataFrame según los valores seleccionados
    gins_filtrados = df[df[columna_elegida].isin(valores_seleccionados)]
    #st.dataframe(gins_filtrados[['Título', 'Productor']])
    st.dataframe(gins_filtrados[cols_mostrar])


    # Información detallada de un vino seleccionado
    if not gins_filtrados.empty:
        st.subheader('Detalles del gin seleccionado')
        gins_filtrados['Mostrar'] = gins_filtrados['Denominación'] 


        gin_seleccionado = st.selectbox('Selecciona un gin:', gins_filtrados['Mostrar'].unique(), key='prod')
        if gin_seleccionado:
            detalles_vino = gins_filtrados[gins_filtrados['Mostrar'] == gin_seleccionado].iloc[0]
            st.dataframe(detalles_vino)
