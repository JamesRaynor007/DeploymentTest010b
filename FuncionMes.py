from fastapi import FastAPI, HTTPException
import pandas as pd
import os

# Definir la ruta del archivo CSV
file_path = os.path.join(os.path.dirname(__file__), 'TotalPeliculasMes.csv')

# Cargar el dataset
try:
    df = pd.read_csv(file_path)
except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error al cargar el archivo: {str(e)}")

# Verificar las columnas del DataFrame
if 'Month' not in df.columns or 'Count' not in df.columns:
    raise HTTPException(status_code=500, detail="El DataFrame no contiene las columnas esperadas.")

# Crear un diccionario para mapear meses en español a meses en inglés
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

# Cambia esta variable según sea necesario para tu entorno de ejecución
BASE_URL = "http://localhost:8000"  # Cambia a tu dominio o IP

@app.get("/")
def read_root():
    return {
        "message": "Bienvenido a la API de películas.",
        "instructions": "Usa el endpoint /peliculas/?mes=nombre_del_mes para obtener datos.",
        "example": "Por ejemplo, para obtener el conteo de películas de enero, visita /peliculas/?mes=enero",
        "links": [
            {"mes": "enero", "url": f"{BASE_URL}/peliculas/?mes=enero"},
            {"mes": "febrero", "url": f"{BASE_URL}/peliculas/?mes=febrero"},
            {"mes": "marzo", "url": f"{BASE_URL}/peliculas/?mes=marzo"},
            {"mes": "abril", "url": f"{BASE_URL}/peliculas/?mes=abril"},
            {"mes": "mayo", "url": f"{BASE_URL}/peliculas/?mes=mayo"},
            {"mes": "junio", "url": f"{BASE_URL}/peliculas/?mes=junio"},
            {"mes": "julio", "url": f"{BASE_URL}/peliculas/?mes=julio"},
            {"mes": "agosto", "url": f"{BASE_URL}/peliculas/?mes=agosto"},
            {"mes": "septiembre", "url": f"{BASE_URL}/peliculas/?mes=septiembre"},
            {"mes": "octubre", "url": f"{BASE_URL}/peliculas/?mes=octubre"},
            {"mes": "noviembre", "url": f"{BASE_URL}/peliculas/?mes=noviembre"},
            {"mes": "diciembre", "url": f"{BASE_URL}/peliculas/?mes=diciembre"},
        ]
    }

@app.get("/peliculas/")
def get_peliculas(mes: str):
    # Convertir el mes a minúsculas para evitar problemas de mayúsculas
    mes = mes.lower()

    # Verificar si el mes está en el diccionario
    if mes not in meses_map:
        raise HTTPException(status_code=400, detail="Mes no válido. Por favor ingrese un mes en español.")

    # Obtener el mes en inglés
    mes_en_ingles = meses_map[mes]

    # Filtrar el DataFrame para encontrar el conteo de películas
    resultado = df[df['Month'] == mes_en_ingles]

    if resultado.empty:
        return {"mes": mes_en_ingles, "cantidad de películas que fueron estrenadas": 0}

    # Verificar que 'Count' sea numérico
    try:
        cantidad = int(resultado['Count'].values[0])
    except ValueError:
        raise HTTPException(status_code=500, detail="Error al procesar la cantidad de películas.")

    return {
        "mes": mes_en_ingles,
        "cantidad de películas que fueron estrenadas": cantidad
    }
