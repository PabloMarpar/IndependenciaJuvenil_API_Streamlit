import matplotlib
import matplotlib.pyplot as plt
from pandas import DataFrame
matplotlib.use('Agg')
import requests
import pandas as pd
import streamlit as st

url = "http://fastapi:8000/datos_limpios"  # Ajusta el puerto según tu configuración de Docker
st.header("Gráficos generales")
st.sidebar.success("En esta página veremos un vistazo rápido sobre nuestros datos ")
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

    print(response.json())
    # Crear cuatro gráficos
    fig, axs = plt.subplots(2, 3, figsize=(20, 10))
    fig.suptitle('Dashboard 1 -- Visualización inicial de los datos', fontsize=18)

    # Gráfico 1: Renta
    years = renta_data['Periodo'].unique()
    women_data = renta_data[renta_data['Sexo/Brecha de género'] == 'Mujeres'].groupby('Periodo')['Total'].sum()
    women_data_sorted = women_data.sort_values()

    axs[0, 0].plot(years, women_data_sorted, label='Mujeres', color='blue')
    axs[0, 0].set_ylabel('Total')
    axs[0, 0].set_title('Evolución de la Renta para Mujeres de 16 a 29 años')
    axs[0, 0].legend()

    # Gráfico 2: Renta (Hombres)
    men_data = renta_data[renta_data['Sexo/Brecha de género'] == 'Hombres'].groupby('Periodo')['Total'].sum()
    men_data_sorted = men_data.sort_values()


    axs[0, 1].plot(years, men_data_sorted, label='Hombres', color='green')
    axs[0, 1].set_ylabel('Total')
    axs[0, 1].set_title('Evolución de la Renta para Hombres de 16 a 29 años')
    axs[0, 1].legend()

    # Gráfico 3: Edad Media de Maternidad
    # Reemplazar comas por puntos y convertir a tipo float
    maternidad_data[['Todos', 'Primero', 'Segundo', 'Tercero']] = maternidad_data[['Todos', 'Primero', 'Segundo', 'Tercero']].replace(',', '.', regex=True).astype(float)

    # Crear el gráfico de líneas con diferentes colores
    axs[0, 2].plot(maternidad_data['Año'], maternidad_data['Todos'], label='Todos', color='blue')
    axs[0, 2].plot(maternidad_data['Año'], maternidad_data['Primero'], label='Primero', color='green')
    axs[0, 2].plot(maternidad_data['Año'], maternidad_data['Segundo'], label='Segundo', color='orange')
    axs[0, 2].plot(maternidad_data['Año'], maternidad_data['Tercero'], label='Tercero', color='red')
    axs[0, 2].set_title('Evolución de la Maternidad por Orden de Nacimiento')
    axs[0, 2].set_ylabel('Edad Media de Maternidad')
    axs[0, 2].legend()

    # Establecer los límites del eje y para que sean los mismos para todas las líneas
    axs[0, 2].set_ylim(maternidad_data[['Todos', 'Primero', 'Segundo', 'Tercero']].min().min(),
                       maternidad_data[['Todos', 'Primero', 'Segundo', 'Tercero']].max().max())

    # Gráfico 4: Edad de Emancipación
    axs[1, 0].plot(emancipacion_data['Año'], emancipacion_data['España'], color='orange')
    axs[1, 0].set_title('Edad de Emancipación')

    # Gráfico 5: Precio de Vivienda por metro cuadrado
    vivienda = vivienda_data.sort_values(by='Compraventa de viviendas', ascending=True)
    axs[1, 1].bar(vivienda['Año'], vivienda['Compraventa de viviendas'], color='red')
    axs[1, 1].set_title('Precio de Vivienda por m²')

    # Gráfico 6: Paro juvenil
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
    st.markdown( 'Con estos graficos podemos ver como la renta de los jovenes ha caido en picado en los últimos años,'
                  'los precios de las viviendas estan volviendo al punto de la búrbuja inmoviliaria, es verdad que el paro no esta en su peor momento' 
                  ' pero aún así la situación no es ideal. '
                  'Por esto que he comentado vemos que la edad de emancipación no para de subir en los últimos años y tambien relacionado con '
                  'esto nos fijamos en que se tienen los hijos cada vez más tarde por las dificultades económicas. ')

if st.button('Ocultar' if mostrar else    '', key='ocultar_button'):
    mostrar_documentacion = not mostrar