import pandas as pd
import requests
from bs4 import BeautifulSoup


def porcentaje_valores_nulos(dataframe):
    '''
    Función que recibe como parametro un DataFrame y retorna el porcentaje de valores nulos por columna.

    Args:
        dataframe (pd.DataFrame): El DataFrame a analizar.

    '''
    porcentaje_nulos = (dataframe.isnull().sum() / (dataframe.shape[0])) * 100
    
    for columna, porcentaje in porcentaje_nulos.items():
        print(f'La columna {columna} tiene un {porcentaje: .2f} % de valores nulos')


def tamanio_datsets(diccionario):
    '''
    Función que recibe como parametro un diccionario, y retorna el nombre del DataFrame y el tamaño del mismo.

    Args:
        diccionario (dict): El diccionario que contiene los DataFrames a analizar.
    
    Returns:
        str: El nombre del DataFrame y su tamaño.

    '''
    for nombre, dataframe in diccionario.items():
        return f'El tamaño del DataFrame', nombre, 'es:', dataframe.shape

        
def deteccion_columnas_anidadas(df):
    '''
    Función que recibe como parametro un DataFrame, y retorna una lista con las colmunas anidadas del mismo.

    Args:
        df (pd.DataFrame): El DataFrame a analizar.
    
    Returns:
        list: Una lista con las columnas anidadas del DataFrame.

    '''
    columnas_anidadas = []

    for columna in df.columns:
        if any(df[columna].astype(str).str.startswith('[{')) or any(df[columna].astype(str).str.startswith('{')):
            columnas_anidadas.append(columna)
     
    return columnas_anidadas
    

def obtener_anio_lanzamiento(url):
    '''
    Función que recibe como parametro una URL e intenta obtener el año de lanzamiento de un juego a partir de una URL dada.

    Args:
        url (str): La URL de la página web que contiene la información del juego.

    Returns:
        str: El año de lanzamiento del juego si se encuentra, o None si no se puede obtener.

    '''
    try:
        response = requests.get(url)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            game_year_element = soup.find('div', {'class': 'date'})
            if game_year_element:
                game_year = game_year_element.text.strip()
                return game_year
            else:
                return None
        else:
            return None
    except Exception as e:
        print(f"Error en la URL {url}: {str(e)}")
        return None


def tipo_de_datos(df):
    '''
    Función que recibe como parametro un DataFrame, y retorna un diccionario
    con el nombre de la columna y su tipo de dato.

    '''
    diccionario = {"Nombre de la columna":[], "Tipo de dato":[]}

    for columna in df.columns:
        diccionario["Nombre de la columna"].append(columna)
        diccionario["Tipo de dato"].append(df[columna].apply(type).unique())
        
    return pd.DataFrame(diccionario)





