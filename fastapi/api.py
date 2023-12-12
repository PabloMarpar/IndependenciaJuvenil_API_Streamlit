from fastapi import FastAPI,HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
import os
app = FastAPI()


current_dir = os.path.dirname(__file__)

rent_path = os.path.join(current_dir, 'Data', '10941.csv')
mat_path = os.path.join(current_dir, 'Data', 'edad_media_de_maternidad_en_españa_segun_orden_de_nacimiento_del_hijo.csv')
em_path = os.path.join(current_dir, 'Data', 'evolucion_de_la_edad_de_emancipacion_en_las_cuatro_grandes_economias_europeas.csv')
viv_path = os.path.join(current_dir, 'Data', 'evolucion_del_precio_de_la_vivienda_por_m2.csv')
par_path=os.path.join(current_dir,'Data','evolucion_de_la_tasa_de_paro_juvenil.csv')


def load_and_clean_data(rent_path, mat_path, em_path, viv_path,par_path):
    # LImpiamos los datos y los cortamos para que solo esten del 2008 al 2021
    ### RENTA
    renta_b = pd.read_csv(rent_path, encoding='ISO-8859-1', delimiter=';')  # o sep=';'
    renta_b['Periodo'] = pd.to_numeric(renta_b['Periodo'], errors='coerce')
    renta = renta_b[renta_b['Grupos de edad'] == 'De 16 a 29 años']

    ### MATERNIDAD
    maternidad_b = pd.read_csv(mat_path, delimiter=';')
    maternidad_b['Año'] = pd.to_numeric(maternidad_b['Año'], errors='coerce')
    maternidad = maternidad_b[(maternidad_b['Año'] >= 2008) & (maternidad_b['Año'] <= 2021)]

    ### EMANCIPACION
    emancipacion_b = pd.read_csv(em_path, delimiter=';')
    emancipacion_b['Año'] = pd.to_numeric(emancipacion_b['Año'], errors='coerce')
    emancipacion = emancipacion_b[(emancipacion_b['Año'] >= 2008) & (emancipacion_b['Año'] <= 2021)]

    ### PRECIO VIVIENDA
    vivienda_b = pd.read_csv(viv_path, delimiter=';')
    vivienda_b['Año'] = pd.to_numeric(vivienda_b['Año'], errors='coerce')
    vivienda = vivienda_b[(vivienda_b['Año'] >= 2008) & (vivienda_b['Año'] <= 2021)]

    ### PARO JUVENIL
    paro_b = pd.read_csv(par_path, delimiter=';')
    paro_b['Año'] = pd.to_numeric(paro_b['Año'], errors='coerce')
    paro_c = paro_b[(paro_b['Año'] >= 2008) & (paro_b['Año'] <= 2021)]
    paro = paro_c[paro_b['Periodo'] == 'Trimestre 3']

    return renta, maternidad, emancipacion, vivienda, paro


renta, maternidad, emancipacion, vivienda, paro = load_and_clean_data(rent_path, mat_path, em_path, viv_path,par_path)

@app.get("/datos_limpios")
def get_datos_limpios():
    try:
        renta, maternidad, emancipacion, vivienda, paro= load_and_clean_data(rent_path, mat_path, em_path, viv_path, par_path)

        return JSONResponse(content={
            "renta": renta.to_dict(orient="records"),
            "maternidad": maternidad.to_dict(orient="records"),
            "emancipacion": emancipacion.to_dict(orient="records"),
            "vivienda": vivienda.to_dict(orient="records"),
            'paro': paro.to_dict(orient='records')
        })

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/datos_limpios")
async def limpiar_datos(datos: dict):
    try:
        ### Datos de independencia
        datos_independencia = datos.get("Independencia", {})
        df_independencia = pd.DataFrame({
            "Año": [int(datos_independencia.get("España", 0))],
            "Edad al independizarse": [int(datos_independencia.get("Edad al independizarse", 0))]
        })

        ### Datos de hijos
        datos_hijos = datos.get("Hijos", [])
        df_hijos = pd.DataFrame()
        for i, item in enumerate(datos_hijos):
            df_hijos[f"Año_{i + 1}º"] = [int(item.get(f"Año_{i + 1}º", 0))]
            df_hijos[f"{i + 1}º"] = [int(item.get(f"{i + 1}º", 0))]



        return {"Datos enviados correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la limpieza de datos: {str(e)}")