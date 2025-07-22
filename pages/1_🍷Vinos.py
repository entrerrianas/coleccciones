import streamlit as st
import pandas as pd
import plotly.express as px
import scripts.leer_data as sleer 
import scripts.modificaciones as modi

# Cargar el archivo CSV
archivo_csv = 'files/vinos.csv'
#df = pd.read_csv(archivo_csv)
df = sleer.cargar_archivo(archivo_csv)
df = modi.mod_vinos(df)
# Título de la aplicación
st.title('Explorador de Datos')


tab1, tab2, tab3 = st.tabs(["Información general", "Datos particulares", "Gráficos"])

with tab1:

    # Selector de columnas
    columnas_seleccionadas = st.multiselect('Selecciona las columnas', df.columns)
   # Filtrar por columnas seleccionadas
    if columnas_seleccionadas:
        df_filtrado = df[columnas_seleccionadas]
    else:
        df_filtrado = df

    # Mostrar los datos filtrados
    st.dataframe(df_filtrado)

with tab2:
    # Crear una lista desplegable para seleccionar la columna
    columnas = [ 'Denominación','Uva',  'Título', 'Productor', 'Clasificación','Cosecha', 'Tipo',
       'País', 'Descripción', 'Comentarios',  'Provincia', 'Ciudad',]
    columna_elegida = st.selectbox('Selecciona una columna:', columnas, key='columna')

    # Obtener los valores únicos de la columna seleccionada
    valores_columna = sorted(df[columna_elegida].unique())

    # Crear una lista desplegable para seleccionar los valores
    
    # Mostrar checkboxes para seleccionar vinos
    if columna_elegida=='Uva':
        columnas_uva = [ 'Denominación', 'Productor', 'Clasificación','Cosecha']
        c1, c2 = st.columns(2)
        valores_seleccionados = c1.multiselect(f'Selecciona valores de {columna_elegida}:', valores_columna, default='Cabernet Franc')

        # Filtrar el DataFrame según los valores seleccionados
        vinos_filtrados = df[df[columna_elegida].isin(valores_seleccionados)].sort_values(by='Denominación')
        vale_clasi = vinos_filtrados['Clasificación'].dropna().unique().tolist()
        default_seleccion = vale_clasi if len(vale_clasi) > 0 else 'nan'
        vale_clasi = vale_clasi if len(vale_clasi) > 0 else [] 
        tiene_nan = vinos_filtrados['Clasificación'].isna().any()
        if tiene_nan and len(vale_clasi) > 0:  # Añadir NaN solo si hay otras clasificaciones
            vale_clasi.append("Sin clasificación")
        
        if len(vale_clasi) > 0:
            clasi_uva = c2.multiselect(f'Selecciona la clasificación:',vale_clasi, default=default_seleccion  )
            if clasi_uva:
                condicion = vinos_filtrados['Clasificación'].isin(clasi_uva)
                if tiene_nan and "Sin clasificación" in clasi_uva:
                    condicion |= vinos_filtrados['Clasificación'].isna()
            
                vinos_filtrados = vinos_filtrados[condicion].sort_values(by='Denominación')
        
        
        mostrar_expander = st.radio(
                "¿Querés filtrar algunos?",
                options=["Sí", "No"],
                index=1  # "No" seleccionado por defecto
)

        if mostrar_expander == "Sí":
            with st.expander("Motrar filtro?:"):
                if valores_seleccionados:
                
                    vinos_uva = c1.multiselect(f'Selecciona valores de {valores_seleccionados} :', 
                                        vinos_filtrados.Título)
                    vinos_filtrados = vinos_filtrados[vinos_filtrados['Título'].isin(vinos_uva)].sort_values(by='Título')
        st.dataframe(vinos_filtrados[columnas_uva])

        
        
        
            
        
    else:
        valores_seleccionados = st.multiselect(f'Selecciona valores de {columna_elegida}:', valores_columna)

        # Filtrar el DataFrame según los valores seleccionados
        vinos_filtrados = df[df[columna_elegida].isin(valores_seleccionados)].sort_values(by='Denominación')
        seleccionados = {}
        st.write(f'cant selecc {len(vinos_filtrados)}')
        if len(vinos_filtrados) > 1:
            with st.expander("Selecciona los vinos que deseas ver en detalle:"):
                for i, row in vinos_filtrados.iterrows():
                    seleccionados[i] = st.checkbox(f"{row['Denominación']} - {row['Productor']} ({row['Variedad']})", key=f"chk_{i}")
                seleccionados_df = vinos_filtrados.loc[[i for i in seleccionados if seleccionados[i]]]
            if st.button("Mostrar información de seleccionados"):
                if not seleccionados_df.empty :
                    st.write("### Vinos seleccionados")
                    st.dataframe(seleccionados_df)  # Muestra toda la info de los seleccionados
                else:
                    st.warning("No seleccionaste ningún vino.")
        else:
            st.write(columnas_seleccionadas)
            st.write(vinos_filtrados[columnas])
    
    # Mostrar tabla con vinos filtrados
    #st.table(vinos_filtrados[['Denominación', 'Productor', 'Variedad']])

    # Información detallada de un vino seleccionado
    if not vinos_filtrados.empty:
        st.subheader('Detalles del vino seleccionado')
        vinos_filtrados['Mostrar'] = vinos_filtrados['Productor'] + ' - ' + vinos_filtrados['Uva']


        vino_seleccionado = st.selectbox('Selecciona un vino:', vinos_filtrados['Mostrar'].unique(), key='prod')
        if vino_seleccionado:
            detalles_vino = vinos_filtrados[vinos_filtrados['Mostrar'] == vino_seleccionado].iloc[0]
            st.write(detalles_vino[columnas_uva])
   
    # Gráfico interactivo
    st.subheader('Gráfico')
    figura = px.bar(df, x='Variedad', y='Provincia',  labels={'Variedad': 'Provincia'})
    st.plotly_chart(figura)
with tab3:

    # Ejemplo de DataFrame de vinos
    # Cargar el archivo CSV

    

    df['Cosecha'] = df['Cosecha'].astype(str)
    # Sidebar para filtrar por provincia
    provincia_seleccionada = st.sidebar.selectbox('Selecciona una provincia:', df['Provincia'].unique())
    vinos_filtrados = df[df['Provincia'] == provincia_seleccionada]

    # Histograma de Cosechas
    st.subheader('Histograma de Cosechas')
    fig_hist = px.histogram(vinos_filtrados, x='Cosecha')
    st.plotly_chart(fig_hist)

    # Gráfico de Barras para Variedades
    st.subheader('Gráfico de Barras para Variedades')
    fig_barras_variedades = px.bar(vinos_filtrados, x='Variedad', title='Cantidad de Vinos por Variedad')
    st.plotly_chart(fig_barras_variedades)

    # Mapa de Variedades por Provincia
    st.subheader('Mapa de Variedades por Provincia')
    fig_mapa_variedades = px.scatter_geo(
        vinos_filtrados,
        locations='Provincia',
        color='Variedad',
        title='Variedades de Uva por Provincia',
    )
    st.plotly_chart(fig_mapa_variedades)

    # Gráfico de Torta para Tipos de Vino
    st.subheader('Gráfico de Torta para Tipos de Vino')
    fig_tarta_tipos = px.pie(vinos_filtrados, names='Tipo', title='Distribución de Tipos de Vino')
    st.plotly_chart(fig_tarta_tipos)


    # Conteo de Productores por Ciudad
    provincia_seleccionada = st.selectbox('Selecciona una provincia:', df['Provincia'].unique(), key='prov')
    vinos_de_provincia = df[df['Provincia'] == provincia_seleccionada]

    st.subheader('Conteo de Productores por Ciudad')
    conteo_productores_ciudad = vinos_de_provincia['Ciudad'].value_counts()
    st.bar_chart(conteo_productores_ciudad)

    # Mapa de Cantidad de Variedades por Provincia
    # st.subheader('Mapa de Cantidad de Variedades por Provincia')
    # fig_mapa_variedades = px.choropleth(
    #     df_vinos,
    #     locations='Provincia',
    #     color=df_vinos.groupby('Provincia')['Uva'].nunique(),
    #     title='Cantidad de Variedades por Provincia',
    # )
    #st.plotly_chart(fig_mapa_variedades)

    # Gráfico de Barras Apiladas para Variedades y Tipos
    st.subheader('Gráfico de Barras Apiladas para Variedades y Tipos')
    fig_barras_apiladas = px.bar(
        vinos_filtrados,
        x='Variedad',
        color='Tipo',
        title='Distribución de Variedades por Tipo de Vino',
        barmode='stack',
    )
    st.plotly_chart(fig_barras_apiladas)
    # Gráfico de Barras Apiladas para Uva y Tipos
    st.subheader('Gráfico de Barras Apiladas para Variedades y Tipos')
    fig_barras_apiladas = px.bar(
        df,
        x='Provincia',
        color='Uva',
        title='Distribución de Uva por Tipo de Vino',
        barmode='stack',
    )
    st.plotly_chart(fig_barras_apiladas)