import matplotlib
import matplotlib.pyplot as plt
from pandas import DataFrame
matplotlib.use('Agg')
import requests
import pandas as pd
import streamlit as st



url = "http://fastapi:8000/datos_limpios"
st.header("Gráficos generales")
st.sidebar.success("En esta página veremos un vistazo rápido sobre nuestros datos ")
try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    if response.status_code == 200:
        renta_data = pd.DataFrame(data["renta"])
        maternidad_data = pd.DataFrame(data["maternidad"])
        emancipacion_data = pd.DataFrame(data["emancipacion"])
        vivienda_data: DataFrame = pd.DataFrame(data["vivienda"])
        paro_data: DataFrame = pd.DataFrame(data['paro'])
    else:
        print(f'Solicitud no exitosa. Código de estado: {response.status_code}')

    print(response.json())
    ### GRAFICOS

    plt.style.use('seaborn-dark')
    plt.rcParams['figure.facecolor'] = '#0c1215'  # Fondo personalizado
    plt.rcParams['axes.facecolor'] = '#0c1215'
    plt.rcParams['text.color'] = 'white'
    plt.rcParams['axes.labelcolor'] = 'white'
    plt.rcParams['xtick.color'] = 'white'
    plt.rcParams['ytick.color'] = 'white'
    fig, axs = plt.subplots(2, 3, figsize=(20, 10))
    fig.suptitle('Dashboard 1 -- Visualización inicial de los datos', fontsize=18)

    ### GRAFICO 1
    years = renta_data['Periodo'].unique()
    women_data = renta_data[renta_data['Sexo/Brecha de género'] == 'Mujeres'].groupby('Periodo')['Total'].sum()
    women_data_sorted = women_data.sort_values()

    axs[0, 0].plot(years, women_data_sorted, label='Mujeres', color='blue')
    axs[0, 0].set_ylabel('Total')
    axs[0, 0].set_title('Evolución de la Renta para Mujeres de 16 a 29 años')
    axs[0, 0].legend()

    ### GRAFICO 2
    men_data = renta_data[renta_data['Sexo/Brecha de género'] == 'Hombres'].groupby('Periodo')['Total'].sum()
    men_data_sorted = men_data.sort_values()


    axs[0, 1].plot(years, men_data_sorted, label='Hombres', color='green')
    axs[0, 1].set_ylabel('Total')
    axs[0, 1].set_title('Evolución de la Renta para Hombres de 16 a 29 años')
    axs[0, 1].legend()

    ### GRAFICA 3
    maternidad_data[['Todos', 'Primero', 'Segundo', 'Tercero']] = maternidad_data[['Todos', 'Primero', 'Segundo', 'Tercero']].replace(',', '.', regex=True).astype(float)

    axs[0, 2].plot(maternidad_data['Año'], maternidad_data['Todos'], label='Todos', color='blue')
    axs[0, 2].plot(maternidad_data['Año'], maternidad_data['Primero'], label='Primero', color='green')
    axs[0, 2].plot(maternidad_data['Año'], maternidad_data['Segundo'], label='Segundo', color='orange')
    axs[0, 2].plot(maternidad_data['Año'], maternidad_data['Tercero'], label='Tercero', color='red')
    axs[0, 2].set_title('Evolución de la Maternidad por Orden de Nacimiento')
    axs[0, 2].set_ylabel('Edad Media de Maternidad')
    axs[0, 2].legend()

    axs[0, 2].set_ylim(maternidad_data[['Todos', 'Primero', 'Segundo', 'Tercero']].min().min(),
                       maternidad_data[['Todos', 'Primero', 'Segundo', 'Tercero']].max().max())

    ### GRAFICO 4
    axs[1, 0].plot(emancipacion_data['Año'], emancipacion_data['España'], color='orange')
    axs[1, 0].set_title('Edad de Emancipación')

    ### GRAFICO 5
    vivienda = vivienda_data.sort_values(by='Compraventa de viviendas', ascending=True)
    axs[1, 1].bar(vivienda['Año'], vivienda['Compraventa de viviendas'], color='red')
    axs[1, 1].set_title('Precio de Vivienda por m²')

    ### GRAFICO 6
    paro_data_sorted = paro_data.sort_values(by='Tasa de paro juvenil', ascending=True)
    axs[1, 2].bar(paro_data_sorted['Año'], paro_data_sorted['Tasa de paro juvenil'], color='b')
    axs[1, 2].set_title('Tasa de Paro Juvenil por Año (Trimestre 3)')
    axs[1, 2].set_ylabel('Tasa de Paro Juvenil')

    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot(fig)

except requests.exceptions.RequestException as e:
    print(f"Error al obtener datos de la API: {e}")

mostrar= st.button("Análisis Gráficas")
if mostrar:
    st.markdown( '''
    Los gráficos presentados muestran una tendencia preocupante en la situación económica de los jóvenes en España. 
 Este descenso se debe a varios factores, entre los que se encuentran la pérdida de poder adquisitivo ,
 el aumento del paro juvenil y la precariedad laboral.
 
 Por otro lado, los precios de la vivienda han vuelto a los niveles de la burbuja inmobiliaria, 
 lo que dificulta aún más el acceso a la vivienda por parte de los jóvenes
 
El retraso de la emancipación también tiene un impacto en la natalidad. Los jóvenes que se emancipan más tarde suelen 
tener hijos más tarde, lo que contribuye a la disminución de la natalidad en España.

En conclusión, la situación económica de los jóvenes en España es preocupante. El descenso de la renta, 
el aumento del paro y la subida de los precios de la vivienda dificultan el acceso a la vivienda y la emancipación de los jóvenes, 
lo que tiene un impacto negativo en la natalidad.
    ''')

if st.button('Ocultar' if mostrar else    '', key='ocultar_button'):
    mostrar_documentacion = not mostrar