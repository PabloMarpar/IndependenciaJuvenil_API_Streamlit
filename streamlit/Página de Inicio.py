
import streamlit as st
import time

# Load the theme
theme = "config.toml"

st.set_page_config(page_title='Estudio Jovenes ', layout='wide',     page_icon="🏠")
ancho = 720
st.image('ufv.png', width=ancho)



placeholder = st.empty()
with placeholder:
    for seconds in range(5):
        placeholder.write(f"⏳ {seconds} Cargando sistema")
        time.sleep(1)
placeholder.empty()



st.sidebar.success("Estás en la página de inicio, seleccione el primer dashboard para continuar")

mostrar_documentacion = st.button("Mostrar Documentación")


if mostrar_documentacion:
    st.markdown(
        """
        En esta práctica voy a usar cinco conjuntos de datos.
         Con estos datos quiero estudiar la situacion actual de la junventud en relación al paso a la 'vida adulta' estudiando datos de estos últimos 13 años. 
        Los cuatro conjuntos tratan sobre : 'Evolución de la renta 16-29 años', 'Evolución de la edad de maternidad', 'Evolución de la edad de emancipación', 'Evolución en la tasa de paro juvenil' y 'Evolución del precio de las viviendas' .
    
        EL primero de ellos 'Evolución de la renta 16-29 años' tiene cuatro variables (Sexo/Brecha de género;Grupos de edad;Periodo;Total) de este conjunto voy a usar todas las variables, he acotado los datos a el grupo de edad de 16 a 29 años 
        y he usado los dos generos. Este conjunto lo he sacado del datos.gob.es 
    
        El segundo 'Evolución de la edad de maternidad' con este quiero ver como afectan los datos que estudiamos al paso de tener un hijo. Las variables son ("Año";"Periodo";"Todos";"Primero";"Segundo";"Tercero";"Cuarto y más") en este caso he 
       usado todas las variables exepto 'cuatro y más' y he acotado los años a 2008-2021 para poder estudiarlo con los demas datos, este conjunto lo he sacado de www.epdata.es 
    
        El tercero 'Evolución de la edad de emancipación', las variables son ("Año";"Periodo";"UE-27";"Alemania";"España";"Francia";"Italia") en este caso he usado las variables 'Año' y 'España' ya que el estudio trata solo de españa 
        y no de una comparación entre naciones, este también es de www.epdata.es 
        
        El cuarto 'Evolución en la tasa de paro juvenil' tiene tres variables (Año";"Periodo";"Tasa de paro juvenil"), he acortado los años como en los demas casos y he tenido en cuenta solo el tercer trimestre, estos datos los he sacado de nuevo de www.epdata.es 
    
        Y finalmente 'Evolución del precio de las viviendas' este tiene estas variables ("Año";"Periodo";"Compraventa de viviendas") he usado 'Año' y 'Compraventa de viviendas' , Compraventa de viviendas es el precio por metro cuadrado, 
        también sacado de www.epdata.es 
        Todos ellos eran archivos del tipo CSV.
    """
    )


if st.button('Ocultar' if mostrar_documentacion else    '', key='ocultar_button'):
    mostrar_documentacion = not mostrar_documentacion

