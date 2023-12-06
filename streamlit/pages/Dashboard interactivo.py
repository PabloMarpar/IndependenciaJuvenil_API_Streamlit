import matplotlib
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
from pandas import DataFrame
import requests

url = "http://fastapi:8000/datos_limpios"
st.header("Gráficos interactivos")
st.sidebar.success("En esta página veremos combinaciones de graficos de tipo interactivo, para hacer más visual sus relaciones")
try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    if response.status_code == 200:
        # Obtener los datos del cuerpo de la respuesta
        renta_data = pd.DataFrame(data["renta"])
        maternidad_data = pd.DataFrame(data["maternidad"])
        emancipacion_data = pd.DataFrame(data["emancipacion"])
        vivienda_data: DataFrame = pd.DataFrame(data["vivienda"])
        paro_data: DataFrame = pd.DataFrame(data['paro'])
    else:
        # La solicitud no fue exitosa, imprime un mensaje o realiza alguna acción
        print(f'Solicitud no exitosa. Código de estado: {response.status_code}')


    #### GRAFICO 1
    # Crear una única figura para los gráficos de renta para mujeres y hombres
    fig_combined_renta = go.Figure()

    years = renta_data[renta_data['Sexo/Brecha de género'] == 'Mujeres']['Periodo'].unique()
    women_data = renta_data[renta_data['Sexo/Brecha de género'] == 'Mujeres'].groupby('Periodo')['Total'].sum()
    women_data_sorted = women_data.sort_values()

    fig_combined_renta.add_trace(
        go.Scatter(x=years, y=women_data_sorted, mode='lines', name='Mujeres', line=dict(color='blue')))

    men_data = renta_data[renta_data['Sexo/Brecha de género'] == 'Hombres'].groupby('Periodo')['Total'].sum()
    men_data_sorted = men_data.sort_values()

    fig_combined_renta.add_trace(
        go.Scatter(x=years, y=men_data_sorted, mode='lines', name='Hombres', line=dict(color='green')))

    # Actualizar el diseño de la figura
    fig_combined_renta.update_layout(title='Evolución de la Renta para Mujeres y Hombres de 16 a 29 años',
                                     yaxis_title='Total')

    # Mostrar el gráfico combinado en Streamlit
    st.plotly_chart(fig_combined_renta)

    boton1 = st.button("Análisis")
    if boton1:
        st.markdown('''
        En este gráfico podemos ver que no es cosa de géneros , desde el 2008 
         los jóvenes independientemente de su sexo han perdido poder adquisitivo, sin tener en cuenta
         la perdida de poder adquisitivo por la inflación, pero eso afecta a todos por igual.''')
    if st.button('Ocultar' if boton1 else '', key='ocultar_button'):
        boton1 = not boton1


            ### GRAFICO 2
    fig_combined = go.Figure()
    maternidad_data[['Todos', 'Primero', 'Segundo', 'Tercero']] = maternidad_data[
        ['Todos', 'Primero', 'Segundo', 'Tercero']].replace(',', '.', regex=True).astype(float)
    # Gráfico de Renta para Mujeres
    years_renta = renta_data['Periodo'].unique()
    women_data = renta_data[renta_data['Sexo/Brecha de género'] == 'Mujeres'].groupby('Periodo')['Total'].sum()
    women_data_sorted = women_data.sort_values()

    fig_combined.add_trace(
        go.Scatter(x=years_renta, y=women_data_sorted, mode='lines', name='Renta - Mujeres', line=dict(color='red')))

    # Gráfico de Maternidad para el Primer Hijo
    fig_combined.add_trace(
        go.Scatter(x=maternidad_data['Año'], y=maternidad_data['Primero'], mode='lines', name='Maternidad - Primero',
                   line=dict(color='green')))

    # Actualizar el diseño de la figura
    fig_combined.update_layout(title='Evolución de la Renta y Maternidad', yaxis_title='Total/Edad Media de Maternidad')

    # Mostrar el gráfico combinado en Streamlit
    st.plotly_chart(fig_combined)

    boton2=st.button('Análisis',key='analisis_button')
    if boton2:
        st.markdown('''
        En esta segunda gráfica podemos ver como mientras baja la renta de las mujeres, 
        la edad de su primer hijo se retrasa. Tener un hijo es un gasto y al parecer esta generación no puede permitirselo hasta los 30 y subiendo.
        ''')
    if st.button('Ocultar' if boton2 else '', key='ocultar_button2'):
        boton2 = not boton2


    ### GRAFICO 3
    # Crear una única figura para todos los gráficos
    fig_em = go.Figure()
    emancipacion_data[['España']] = emancipacion_data[
        ['España']].replace(',', '.', regex=True).astype(float)

    # Gráfico de Maternidad para el Primer Hijo
    fig_em.add_trace(
        go.Scatter(x=maternidad_data['Año'], y=maternidad_data['Primero'], mode='lines', name='Maternidad - Primero',
                   line=dict(color='green')))

    # Gráfico de Edad de Emancipación
    fig_em.add_trace(
        go.Scatter(x=emancipacion_data['Año'], y=emancipacion_data['España'], mode='lines', name='Edad de Emancipación',
                   line=dict(color='orange')))

    # Actualizar el diseño de la figura
    fig_em.update_layout(title='Evolución de Maternidad y Edad de Emancipación',
                               yaxis_title='Edad Media de Maternidad/Edad de Emancipación')

    # Mostrar el gráfico combinado en Streamlit
    st.plotly_chart(fig_em)

    boton3=st.button('Análisis',key='Boton 3')
    if boton3:
        st.markdown('''
        Ahora observamos la relación que tiene la emancipación con la decisión de tener un hijo, 
        podemos ver como cuanto mas tarde nos emancipamos mas tarde tenemos el primer hijo.
        ''')
    if st.button('Ocultar' if boton3 else '', key='ocultar_button3'):
        boton3 = not boton3



except requests.exceptions.RequestException as e:
    print(f"Error al obtener datos de la API: {e}")