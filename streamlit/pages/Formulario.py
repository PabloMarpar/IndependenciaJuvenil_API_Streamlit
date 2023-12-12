import streamlit as st

if 'data_history' not in st.session_state:
    st.session_state.data_history = []

def es_numero_entero(cadena):
    return cadena.isdigit()

### FORMULARIO INDEPENDENCIA
año_independencia = st.text_input("Año de independencia:", key="año_independencia")
edad_independencia = st.text_input("Edad al independizarse:", key="edad_independencia")

if es_numero_entero(año_independencia) and es_numero_entero(edad_independencia):
    año_independencia = int(año_independencia)
    edad_independencia = int(edad_independencia)
else:
    st.write("Por favor, ingresa valores numéricos válidos para el año y la edad.")

### FORMULARIO HIJOS
tiene_hijos = st.radio("¿Tienes hijos?", ["Sí", "No"], index=1)

if tiene_hijos == "Sí":
    num_hijos = st.number_input("Número de hijos:", 1, 3, 1)

    datos_hijos = []
    for i in range(num_hijos):
        st.header(f"Datos del {i + 1}º hijo")
        año_hijo = st.text_input(f"Año del {i + 1}º hijo:", key=f"año_hijo_{i}")

        if es_numero_entero(año_hijo):
            año_hijo = int(año_hijo)
        else:
            st.write(f"Por favor, ingresa un valor numérico válido para el año del {i + 1}º hijo.")

        edad_hijo = st.text_input(f"Edad al tener el {i + 1}º hijo:", key=f"edad_hijo_{i}")

        if es_numero_entero(edad_hijo):
            edad_hijo = int(edad_hijo)
        else:
            st.write(f"Por favor, ingresa un valor numérico válido para la edad del {i + 1}º hijo.")

        datos_hijos.append({f"Año_{i + 1}º": año_hijo, f"{i + 1}º": edad_hijo})

else:
    datos_hijos = []



if st.button("Enviar Datos"):

    datos_independencia = {
        "España": año_independencia,
        "Edad al independizarse": edad_independencia
    }

    datos_hijos_dict = [
        {f"Año_{i + 1}º": item[f"Año_{i + 1}º"], f"{i + 1}º": item[f"{i + 1}º"]} for i, item in enumerate(datos_hijos)
    ]

    datos_actual = {
        "Independencia": datos_independencia,
        "Hijos": datos_hijos_dict
    }

    st.session_state.data_history.append(datos_actual)

    st.success("Datos enviados correctamente.")


if st.button("Quiere ver los datos recopilados?"):
    st.table(st.session_state.data_history)
