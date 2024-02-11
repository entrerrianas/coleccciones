import streamlit as st
import pandas as pd
import scripts.modificaciones as modificaciones
import scripts.leer_data as sleer 


# Cargar el archivo CSV
archivo_sofia_csv = 'files/libros-sofia.csv'
df_sofia = sleer.cargar_archivo(archivo_sofia_csv)
archivo_gonzalo_csv = 'files/libros-gonzalo.csv'
df_gonzalo = sleer.cargar_archivo(archivo_gonzalo_csv)

df_sofia['fuente'] = 'Sofía'
df_gonzalo['fuente'] = 'Gonzalo'

# Título de la aplicación
st.title('Explorador de Libros')

# Unir los dos DataFrames
df_unido = pd.concat([df_sofia, df_gonzalo], ignore_index=True)

#completar con datos la columna autor
df_unido['Autor'] = df_unido['Autor'].fillna('Sin autor')

#convertir años en enteros
df_unido['Año del copyright'] = df_unido['Año del copyright'].fillna(0).astype(int)
df_unido['Año de publicación'] = df_unido['Año de publicación'].fillna(0).astype(int)

df_unido['Páginas'] = df_unido['Páginas'].fillna(0).astype(int)

tab1, tab2 = st.tabs(["Información general", "Datos particulares"])

with tab1:
    # Mostrar el DataFrame resultante
    st.write(df_unido)
    # Selector de columnas
    columnas_seleccionadas = st.multiselect('Selecciona las columnas', df_unido.columns)
   # Filtrar por columnas seleccionadas
    if columnas_seleccionadas:
        df_filtrado = df_unido[columnas_seleccionadas]
    else:
        df_filtrado = df_unido

    # Mostrar los datos filtrados
    st.dataframe(df_filtrado)

with tab2:
    columnas_interesantes = ['Título', 'Autor', 'Editor', 'Encuadernación',
        'Editorial', 'Edición', 'Año de publicación', 'ISBN#', 
       'Traductor', 'Idioma', 'Género', 'Palabras clave', 'Serie',
        'Condición',  'Sinopsis',
       'Comentarios', 'Fecha de creación', 'Fecha de modificación',
       'País Autor', 'fuente']

    # Crear una lista desplegable para seleccionar la columna
    columna_elegida = st.selectbox('Selecciona una columna:', columnas_interesantes, key='columnas_datos')
    if columna_elegida == 'Autor' or columna_elegida == 'Palabras clave':
        # Realizar acciones específicas para la columna 'Autor' o Palabras Clave
        df_unido = df_unido.dropna(subset=['Palabras clave'])
        lista_total_columna = df_unido[columna_elegida].apply(lambda x: x.split(';')).explode().tolist()
        valores_unicos = sorted(set(list(map(lambda x: x.strip() if isinstance(x, str) else x, lista_total_columna))))
    else:
        # Obtener los valores únicos de otras columnas
        valores_unicos = sorted(df_unido[columna_elegida].dropna().unique())
    #genero una lista con la letra con que comienza los valores unicos
    opciones = list(sorted(set((map(lambda x:modificaciones.sacar_acento(x[0].strip().upper()), valores_unicos)))))

    # agrego todos
    opciones =  ['Todos'] + opciones
    # Desplazador para seleccionar la letra inicial
    letra_inicial = st.select_slider('Selecciona la letra inicial', options=opciones)

    # Filtrar opciones según la letra seleccionada
    if letra_inicial == 'Todos':
        valores_seleccionados = st.multiselect(f'Selecciona valores de {columna_elegida}:', valores_unicos)
    else:
        opciones_filtradas = [opcion for opcion in valores_unicos if opcion.startswith(letra_inicial)]
        valores_seleccionados = st.multiselect(f'Selecciona valores de {columna_elegida}:', opciones_filtradas)


   

    # Crear una lista desplegable para seleccionar los valores
    if valores_seleccionados:
        lista_valores_str = [str(valor) for valor in valores_seleccionados]
        # Filtrar el DataFrame según los valores seleccionados
        df_filtrado = df_unido[df_unido[columna_elegida].astype(str).str.contains('|'.join(lista_valores_str))]

    # Mostrar los datos filtrados
    st.write(df_filtrado)
    if not df_filtrado.empty:
        st.subheader('Detalles del libro seleccionado')
        libro_seleccionado = st.selectbox('Selecciona un libro:', df_filtrado['Título'].unique(), key='titulo')
        if libro_seleccionado:
            
            columnas_seleccionadas = st.multiselect('Selecciona las columnas', df_unido.columns, key='columnas_sele')
            if columnas_seleccionadas:
                columnas_seleccionadas = columnas_seleccionadas if 'Título' in columnas_seleccionadas else columnas_seleccionadas + ['Título']
                df_filtrado = df_filtrado[columnas_seleccionadas]
                detalles_libro = df_filtrado[df_filtrado['Título'] == libro_seleccionado].iloc[0]
                
            else:
                df_filtrado = df_unido
                detalles_libro = df_filtrado[df_filtrado['Título'] == libro_seleccionado].iloc[0]
            for columna, valor in detalles_libro.items():
                st.text(f"{columna}: {valor}")
            #st.write(detalles_libro)

