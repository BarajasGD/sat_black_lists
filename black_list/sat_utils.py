# app_sat/sat_utils.py
import pandas as pd
import requests
from io import StringIO
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

# URLs de las listas
LISTAS_URLS = {
    "NoLocalizados": "https://wu1aqauatsta002.blob.core.windows.net/datosabiertos/No%20localizados.csv",
    "Sentencias": "https://wu1aqauatsta002.blob.core.windows.net/datosabiertos/Sentencias.csv",
    "Cancelados": "https://wu1aqauatsta002.blob.core.windows.net/datosabiertos/Cancelados.csv"
}

def consultar_lista_sat(rfc, lista_nombre):
    """
    Consulta solo una lista específica
    Devuelve: {
        'encontrado': bool,
        'registros': [dict],
        'error': str|None
    }
    """
    resultado = {
        'encontrado': False,
        'registros': [],
        'error': None
    }

    if lista_nombre not in LISTAS_URLS:
        resultado['error'] = f"Lista {lista_nombre} no válida"
        return resultado

    try:
        url = LISTAS_URLS[lista_nombre]
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=20)
        
        if response.status_code == 200:
            df = pd.read_csv(
                StringIO(response.text),
                encoding='latin-1',
                delimiter=',',
                header=0,
                dtype=str
            )
            
            # Limpieza de datos
            df = df.rename(columns={df.columns[0]: 'RFC'})
            df['RFC'] = df['RFC'].str.strip().str.upper()
            
            # Filtrar por RFC
            registros = df[df['RFC'] == rfc.strip().upper()]
            
            if not registros.empty:
                resultado['encontrado'] = True
                # Convertir a lista de diccionarios y limpiar nombres de columnas
                resultado['registros'] = registros.rename(columns={
                    'RAZÓN SOCIAL': 'razon_social',
                    'SUPUESTO': 'supuesto',
                    'FECHAS DE PRIMERA PUBLICACION': 'fecha_publicacion'
                }).to_dict('records')
        
        else:
            resultado['error'] = f"Error HTTP {response.status_code} al consultar {lista_nombre}"
    
    except Exception as e:
        resultado['error'] = str(e)
        logger.error(f"Error consultando {lista_nombre}: {str(e)}")
    
    return resultado