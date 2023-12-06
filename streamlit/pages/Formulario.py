import streamlit as st
import requests
st.title("Formulario de Datos")

# Formulario para datos de independencia
año_independencia = st.text_input("Año de independencia:", key="año_independencia")
edad_independencia = st.text_input("Edad al independizarse:", key="edad_independencia")

# Formulario para datos de hijos
tiene_hijos = st.radio("¿Tienes hijos?", ["Sí", "No"], index=1)

if tiene_hijos == "Sí":
    num_hijos = st.number_input("Número de hijos:", 1, 3, 1)

    datos_hijos = []
    for i in range(num_hijos):
        st.header(f"Datos del {i + 1}º hijo")
        año_hijo = st.text_input(f"Año del {i + 1}º hijo:", key=f"año_hijo_{i}")
        edad_hijo = st.text_input(f"Edad al tener el {i + 1}º hijo:", key=f"edad_hijo_{i}")
        datos_hijos.append({f"Año_{i + 1}º": año_hijo, f"{i + 1}º": edad_hijo})

else:
    datos_hijos = []

# Botón para enviar los datos
if st.button("Enviar Datos"):
    # Crear diccionarios con los datos recopilados
    datos_independencia = {
        "España": año_independencia,
        "Edad al independizarse": edad_independencia
    }

    datos_hijos_dict = [
        {f"Año_{i + 1}º": item[f"Año_{i + 1}º"], f"{i + 1}º": item[f"{i + 1}º"]} for i, item in enumerate(datos_hijos)
    ]

    # Crear un diccionario con todos los datos recopilados
    datos = {
        "Independencia": datos_independencia,
        "Hijos": datos_hijos_dict
    }


    # Enviar los datos a la API
    url_api = "http://fastapi:8000/datos_limpios"
    respuesta = requests.post(url_api, json=datos)

    # Mostrar la respuesta de la API
    st.success(f"Datos enviados correctamente. Respuesta de la API: {respuesta.text}")
