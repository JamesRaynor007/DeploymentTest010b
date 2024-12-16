from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import pandas as pd
import os

# Define the path for the CSV file
file_path = os.path.join(os.path.dirname(__file__), 'TotalPeliculasMes.csv')

# Create a dictionary to map Spanish months to English months
meses_map = {
    'enero': 'January',
    'febrero': 'February',
    'marzo': 'March',
    'abril': 'April',
    'mayo': 'May',
    'junio': 'June',
    'julio': 'July',
    'agosto': 'August',
    'septiembre': 'September',
    'octubre': 'October',
    'noviembre': 'November',
    'diciembre': 'December'
}

app = FastAPI()

class PeliculasResponse(BaseModel):
    mes: str
    cantidad_de_peliculas: int

@app.get("/", response_model=dict)
def read_root(request: Request):
    base_url = f"{request.url.scheme}://{request.url.netloc}"
    return {
        "message": "Bienvenido a la API de películas.",
        "instructions": "Usa el endpoint /peliculas/?mes=nombre_del_mes para obtener datos.",
        "links": [{"mes": mes, "url": f"{base_url}/peliculas/?mes={mes}"} for mes in meses_map.keys()]
    }


@app.get("/peliculas/", response_model=PeliculasResponse)
def get_peliculas(mes: str):
    mes = mes.lower()
    if mes not in meses_map:
        raise HTTPException(status_code=400, detail="Mes no válido. Por favor ingrese un mes en español.")
    
    # Load the dataset inside the endpoint to handle errors more gracefully
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al cargar el archivo: {str(e)}")

    # Verify the required columns
    if 'Month' not in df.columns or 'Count' not in df.columns:
        raise HTTPException(status_code=500, detail="El DataFrame no contiene las columnas esperadas.")
    
    mes_en_ingles = meses_map[mes]
    resultado = df[df['Month'] == mes_en_ingles]

    if resultado.empty:
        return PeliculasResponse(mes=mes_en_ingles, cantidad_de_peliculas=0)

    try:
        cantidad = int(resultado['Count'].values[0])
    except (ValueError, IndexError) as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la cantidad de películas: {str(e)}")

    return PeliculasResponse(mes=mes_en_ingles, cantidad_de_peliculas=cantidad)
