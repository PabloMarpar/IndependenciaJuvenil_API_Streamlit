import streamlit as st
import requests

# Inicializar la lista de datos si no existe
if 'data_history' not in st.session_state:
    st.session_state.data_history = []

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

    # Crear un diccionario con los datos actuales
    datos_actual = {
        "Independencia": datos_independencia,
        "Hijos": datos_hijos_dict
    }

    # Agregar los datos actuales al historial de sesiones
    st.session_state.data_history.append(datos_actual)

    # Mensaje indicando que los datos se han enviado correctamente
    st.success("Datos enviados correctamente.")

# Botón para mostrar u ocultar la tabla
if st.button("Quiere ver los datos recopilados?"):
    # Mostrar la información en una tabla
    st.table(st.session_state.data_history)
