from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse
import pandas as pd
import numpy as np
import scipy as sp
from sklearn.metrics.pairwise import cosine_similarity
import operator
import pyarrow as pa
import pyarrow.parquet as pq
from scipy.sparse import csr_matrix

app = FastAPI()

df_developer = pd.read_parquet('Data/developer.parquet')
user_reviews = pd.read_parquet('Data/user_reviews.parquet')
df_userdata = pd.read_parquet('Data/userdata.parquet')
df_userforgenre = pd.read_parquet('Data/userforgenre.parquet')
df_bestdeveloperyear = pd.read_parquet('Data/bestdeveloperyear.parquet')
df_developer_reviews = pd.read_parquet('Data/developer_reviews.parquet')
modelo_render = pd.read_parquet('Data/modelo_render.parquet')


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def read_root():
    message = """
    <html>
        <head>
            <style>
                body {
                    font-family: 'Arial', sans-serif;
                    background-color: #FFE7E7; /* Rosa pastel */
                    margin: 0;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    height: 100vh;
                }
                .container {
                    text-align: center;
                    color: #5C5470; /* Gris oscuro */
                    max-width: 600px;
                }
                .logo {
                    width: 100px;
                    height: 100px;
                }
                .welcome {
                    font-size: 36px;
                    font-weight: bold;
                    margin: 20px 0 10px;
                    border-bottom: 2px solid #5C5470; /* Línea de guiones bajos */
                    padding-bottom: 10px;
                }
                .intro {
                    font-size: 18px;
                    margin-bottom: 20px;
                }
                .button-container {
                    text-align: center;
                    margin-top: 20px;
                }
                .button {
                    font-size: 16px;
                    padding: 10px 20px;
                    background-color: #4caf50; /* Verde para resaltar el botón */
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="welcome">MILAGROS TORRES</div>
                <div class="intro">
                    ¡Bienvenido a mi primer proyecto individual!<br>
                    En este proyecto llevo a cabo el papel de un Data Engineer e implemento mis conocimientos en Machine Learning,
                    creando un MVP para ser consumido a través de FastApi. En el siguiente link podrás hacer consultas sobre la plataforma de juegos Steam Games:
                    <a href="https://henry-mlops-pi1-milagros.onrender.com/docs">https://henry-mlops-pi1-milagros.onrender.com/docs</a>
                    El desarrollo de este proyecto lo encuentras en mi repositorio de GitHub: <a href="https://github.com/MiliTrres/Henry-PI1-MLOps-Steam.git">https://github.com/MiliTrres/Henry-PI1-MLOps-Steam.git</a>
                </div>
            </div>
            
        </body>
    </html>
    """
    return HTMLResponse(content=message)



@app.get("/redirect", include_in_schema=False)
def redirect_to_docs():
    link = "https://henry-mlops-pi1-milagros.onrender.com/docs"
    raise HTTPException(status_code=302, detail="Redirecting", headers={"Location": link})


# Endpoint /developer 
@app.get("/developer")
def Developer(desarrollador: str):
    '''
    Función que recibe como parametro el nombre de una empresa desarrolladora, y retorna la cantidad de items y el porcentaje de contenido gratuito por año.

    Args:
        desarrollador (str): Nombre de la empresa desarrolladora.

    Returns:
        dict: Diccionario con la cantidad de items y el porcentaje de contenido gratuito por año.

    Ejemplo:
        'Valve'

    '''

    # Filtrar el DataFrame por desarrollador
    developer = df_developer[df_developer['developer'] == desarrollador]

    # Calcular la cantidad de items por año
    items_por_anio = developer.groupby('release_year')['item_id'].count()

    # Filtrar los items gratuitos y contarlos por año
    free_por_anio = developer[developer['price'] == 0.0].groupby('release_year')['item_id'].count()

    # Calcular el porcentaje de items gratuitos por año
    porcentaje_gratuito = ((free_por_anio / items_por_anio) * 100).fillna(0).astype(int)

    # Retornar los resultados en formato de diccionario
    return {
        'cantidad_por_año': items_por_anio.to_dict(),
        'porcentaje_gratis_por_anio': porcentaje_gratuito.to_dict()
    }

@app.get("/developer/{desarrollador}",
                    description=
                    """ <font color="black">
                    INSTRUCCIONES<br>
                    1. Haga clik en "Try it out".<br>
                    2. Ingrese el nombre de una empresa desarrolladora para obtener la cantidad de items y porcentaje de contenido gratuito por año.  <br>
                    3. Scrollear a "Response body" para ver el resultado.
                    </font>"""
                    , tags=['Consultas generales'])
async def get_developer(desarrollador: str):
    try:
        
        parquet_path = 'Data/developer.parquet'
        
        return Developer(desarrollador)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la solicitud: {str(e)}")

    
# Endpoint /userdata 
@app.get("/userdata")
def UserData(user_id: str):
    '''
    Función que recibe como parametro el ID de un usuario, y retorna el dinero gastado por el usuario, el porcentaje de recomendación en base a las reseñas y cantidad de items.

    Args:
        user_id (str): Identificador único del usuario.
    
    Returns:
        dict: Diccionario con detalles sobre el usuario, incluyendo dinero gastado, items comprados y porcentaje de recomendaciones.

    Ejemplo:
        'GamekungX'

    '''
    # Filtrar el DataFrame de reseñas por el ID de usuario
    user = user_reviews[user_reviews['user_id'] == user_id]

    # Obtener el dinero gastado y items comprados del DataFrame de datos de usuario
    dinero_gastado = df_userdata[df_userdata['user_id'] == user_id]['price'].iloc[0]
    items_comprados = df_userdata[df_userdata['user_id'] == user_id]['items_count'].iloc[0]

    # Calcular la cantidad de recomendaciones y el porcentaje de recomendaciones
    recomendaciones = user['recommend'].sum()
    reviews = len(user_reviews[user_reviews['user_id'] == user_id])
    porcent_recomendaciones = (recomendaciones / reviews) * 100 if reviews > 0 else 0.0

    # Retornar los resultados en formato de diccionario
    return {
        'user_id': user_id,
        'dinero_gastado': dinero_gastado,
        'items_comprados': int(items_comprados),
        '%_recomendaciones': round(porcent_recomendaciones, 3)
    }


@app.get("/userdata/{user_id}",
                    description=
                    """ <font color="black">
                    INSTRUCCIONES<br>
                    1. Haga clik en "Try it out".<br>
                    2. Ingrese un identificador unico de usuario para obtener el dinero gastado, los items comprados y el porcentaje de recomendación del mismo.  <br>
                    3. Scrollear a "Response body" para ver el resultado.
                    </font>"""
                    , tags=['Consultas generales'])
async def get_user_id(user_id: str):
    try:
        parquet_path2 = 'Data/userdata.parquet'
        
        result = UserData(user_id)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# Endpoint /userforgenre 
@app.get("/userforgenre")
def UserForGenre(genre: str):
    '''
    Función que recibe como parametro el nombre de un género, y retorna el usuario con más horas jugadas y la acumulación de horas jugadas por año de lanzamiento.

    Args:
        genre (str): Nombre del género.

    Returns:
        dict: Diccionario con el usuario con más horas jugadas y la acumulación de horas jugadas por año.

    Ejemplo: 
        'Indie'
    
    '''

    # Filtrar el DataFrame por género
    genre_df = df_userforgenre[df_userforgenre['genres'] == genre]

    # Convertir las horas jugadas a formato de horas enteras
    genre_df['playtime_forever'] = (genre_df['playtime_forever'] / 60 / 60).astype(int)

    # Obtener el usuario con más horas jugadas
    max_playtime_user = genre_df.loc[genre_df['playtime_forever'].idxmax(), 'user_id']

    # Calcular la acumulación de horas jugadas por año
    yearly_playtime = genre_df.groupby('release_year')['playtime_forever'].sum().reset_index()

    # Crear una lista de diccionarios con la información de horas jugadas por año
    playtime_list = [{'Año': int(year), 'Horas': int(hours)} for year, hours in zip(yearly_playtime['release_year'], yearly_playtime['playtime_forever'])]


    return {
        "Usuario con más horas jugadas para género " + genre: max_playtime_user, "Horas jugadas": playtime_list
        }

@app.get("/userforgenre/{genre}",
                    description=
                    """ <font color="black">
                    INSTRUCCIONES<br>
                    1. Haga clik en "Try it out".<br>
                    2. Ingrese un genero de juego para obtener el usuario con más horas jugadas y la acumulación de horas jugadas por año. <br>
                    3. Scrollear a "Response body" para ver el resultado.
                    </font>"""
                    , tags=['Consultas generales'])
async def get_userforgenre(genre: str):
    try:
        parquet_path3 = 'Data/userforgenre.parquet'
        
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
#Endpoint /bestdeveloperyear
@app.get("/bestdeveloperyear")  
def BestDeveloperYear(year: int):
    '''
    Función que recibe como parametro un año, y retorna el TOP 3 de desarrolladores con juegos más recomendados por usuarios para el año ingresado.

    Args:
        year (int): Año de lanzamiento de los juegos.
    
    Returns:
        dict: Diccionario con el TOP 3 de desarrolladores con juegos más recomendados por usuarios para el año ingresado.
    
    Ejemplo:
        2017
    
    '''
    
    # Filtrar el DataFrame por año
    anio = df_bestdeveloperyear[df_bestdeveloperyear['release_year'] == year]

    # Filtrar los juegos recomendados y con análisis de sentimiento positivo
    filtro = anio[(anio['sentiment_analysis'] == 2) & (anio['recommend'] == True)]

    # Agrupar por desarrollador y sumar los análisis de sentimiento
    developer = filtro.groupby('developer')['sentiment_analysis'].sum().reset_index()

    # Ordenar en orden descendente según la suma de análisis de sentimiento
    df_ordenado = developer.sort_values(by='sentiment_analysis', ascending=False)

    # Seleccionar los 3 mejores desarrolladores
    top_developers = df_ordenado.head(3)

    # Crear una lista de diccionarios con el resultado
    result = [{"Puesto {}: {}".format(i+1, row['developer'])} for i, (_, row) in enumerate(top_developers.iterrows())]

    return result

@app.get("/bestdeveloperyear/{year}",
                    description=
                    """ <font color="black">
                    INSTRUCCIONES<br>
                    1. Haga clik en "Try it out".<br>
                    2. Ingrese un año para obtener el TOP 3 de desarrolladores con juegos más recomendados por usuarios para el año ingresado <br>
                    3. Scrollear a "Response body" para ver el resultado.
                    </font>"""
                    , tags=['Consultas generales'])
async def getbestdeveloperyear(year: int):
    try:
        parquet_path4 = "Dataset/dataset_endpoint_4.parquet"
        
        result = BestDeveloperYear(year)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
#Endpoint /developerreviewsanalysis
@app.get("/developerreviewsanalysis")
def DeveloperReviewsAnalysis(desarrollador):
    '''
    Funcióon que recibe como parametro el nombre de una empresa desarrolladora, y retorna la cantidad de reseñas positivas y negativas, descartando las neutras.

    Args:
        desarrollador (str): Nombre de la empresa desarrolladora.
    
    Returns:
        dict: Diccionario con la cantidad de reseñas positivas y negativas, descartando las neutras.
    
    Ejemplo:
        'Valve'
    '''

    developer = df_developer_reviews[df_developer_reviews['developer'] == desarrollador]

    positivo = 0
    negativo = 0

    for sentiment in developer['sentiment_analysis']:
        if sentiment == 2:
            positivo += 1
        else:
            negativo += 1

    return {
        desarrollador: [f"Negative = {negativo}", f"Positive = {positivo}"]
    }

@app.get("/developerreviewsanalysis/{desarrollador}",
                    description=
                    """ <font color="black">
                    INSTRUCCIONES<br>
                    1. Haga clik en "Try it out".<br>
                    2. Ingrese el nombre de la empresa desarrolladora para obtener la cantidad de reseñas positivas y negativas. <br>
                    3. Scrollear a "Response body" para ver cuantas reseñas positivas y negativas tuvo el desarrollador.
                    </font>"""
                    , tags=['Consultas generales'])
async def getdeveloperreviewsanalysis(desarrollador: str):
    try:
        parquet_path5 = 'Data/developer_reviews.parquet'
        
        
        result = DeveloperReviewsAnalysis(desarrollador)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    


# Sistema de Recomendación /recommend_games
@app.get("/recommend_games")
def recommend_games(id: int):
    '''
    Función que recibe como parametro el ID de un juego y retorna una lista con los 5 juegos más similares.

    Args:
        id (int): ID del juego.

    Returns:
        dict: Diccionario con los 5 juegos más similares al juego ingresado.

    Ejemplo:
        767400
    '''

    try:
        # Filtrar el DataFrame por el ID del juego
        game = modelo_render[modelo_render['item_id'].astype(int) == id]

        # Verificar si el juego con el ID proporcionado existe
        if game.empty:
            raise ValueError(f"No se encontró un juego con el ID {id}.")

        # Obtener el índice del juego en el DataFrame
        idx = game.index[0]

        # Tamaño de la muestra para calcular similitud
        sample_size = 2000
        df_sample = modelo_render.sample(n=sample_size, random_state=42)

        # Calcular la similitud de coseno entre el juego seleccionado y la muestra
        similitud = cosine_similarity([modelo_render.iloc[idx, 3:]], df_sample.iloc[:, 3:])

        # Obtener la fila de similitud
        similitud = similitud[0]

        # Crear una lista de tuplas (índice, similitud) y ordenarla por similitud descendente
        juegos_similares = [(i, similitud[i]) for i in range(len(similitud)) if i != idx]
        juegos_similares = sorted(juegos_similares, key=lambda x: x[1], reverse=True)

        # Obtener los índices de los juegos más similares
        ind_juegos_similares = [i[0] for i in juegos_similares[:5]]

        # Obtener los nombres de los juegos más similares
        nombre_juegos_similares = df_sample['app_name'].iloc[ind_juegos_similares].tolist()

        return {'Juegos_similares': nombre_juegos_similares}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/recommendgames/{id}",
         description=
         """ <font color="black">
         INSTRUCCIONES<br>
         1. Haga clik en "Try it out".<br>
         2. Ingrese el ID de un juego para obtener el TOP 5 de juegos más similares. <br>
         3. Scrollear a "Response body" para ver los juegos recomendados similares al ingresado.
         </font>""", tags=['Sistema de recomendación'])
async def recommendgames(id: int):
    try:
        return JSONResponse(content={"Juegos_similares": recommend_games(id)})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


