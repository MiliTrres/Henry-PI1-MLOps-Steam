<p align=center><img src=https://github.com/MiliTrres/Henry-PI1-MLOps-Steam/blob/main/Img/68747470733a2f2f643331757a386c77666d796e38672e636c6f756466726f6e742e6e65742f4173736574732f6c6f676f2d68656e72792d77686974652d6c672e706e67.png><p>



# <h1 align=center> **PROYECTO INDIVIDUAL Nº1** </h1>

# <h1 align=center>**`Machine Learning Operations (MLOps)`**</h1>

<p align=center><img src=https://github.com/MiliTrres/Henry-PI1-MLOps-Steam/blob/main/Img/Why%20Is%20There%20A%20Shortage%20Of%20MLOps%20Engineers_.jpg height=300><p>

## Introducción

Este proyecto representa el Producto Individual 1 en el campo de Machine Learning, desarrollado dentro del bootcamp de Henry. Su propósito es simular el rol de un ***MLOps Engineer***, una figura que combina las habilidades de **un Data Engineer + un Data Scientist**. En esta simulación, el MLOps Engineer trabaja para la conocida plataforma de videojuegos, Steam. El proyecto se centra en abordar un desafío empresarial clave: la creación de un Producto Mínimo Viable (MVP) que incorpora tanto una API de implementación, como un modelo de Machine Learning.

## Descripción del proyecto

El proyecto busca solucionar dos problemas esenciales en la plataforma Steam:

**Análisis de Sentimientos de Usuarios:** El primer desafío consiste en analizar y clasificar los comentarios de los usuarios. Para ello, se emplea la librería TextBlob, una herramienta de Procesamiento del Lenguaje Natural (NLP). TextBlob determina la polaridad del sentimiento en cada comentario y lo clasifica como negativo, neutral o positivo.

**Sistema de Recomendación de Juegos:** El segundo desafío, radica en construir un sistema de recomendación de videojuegos. Este sistema proporciona recomendaciones de juegos a los usuarios basándose en sus preferencias y comportamientos anteriores.

## Datos

Para desarrollar el proyecto se utilizaron tres archivos en formato JSON:

**output_steam_games.json**: Contiene información sobre los juegos; el nombre, el editor, el desarrollador, los precios y las etiquetas.

**australian_users_items.json**: Contiene información sobre los juegos utilizados por los usuarios y el tiempo que cada usuario pasa en cada juego.

**australian_users_reviews.json**: Contiene los comentarios que los usuarios realizaron sobre los juegos que usan, así como recomendaciones o críticas sobre esos juegos, ID del usuario y su URL.

## Tareas realizadas

### ETL (Extract, Transform and Load)
![Pandas](https://img.shields.io/badge/-Pandas-333333?style=flat&logo=pandas)
![Numpy](https://img.shields.io/badge/-Numpy-333333?style=flat&logo=numpy)
![VSCode](https://img.shields.io/badge/-VSCode-333333?style=flat&logo=visual-studio-code)
![Jupyter](https://img.shields.io/badge/-Jupyter-333333?style=flat&logo=jupyter)
![Python](https://img.shields.io/badge/-Python-333333?style=flat&logo=python)

En esta fase, se llevo a cabo la ingesta de datos. Se convirtieron los datasets en DataFrames para poder trabajar de manera optima, se desanidaron columnas anidadas, se trasnformaron y limpiaron datos. Para ser más precisos, en esta etapa se realizaron tareas como las siguientes: Análisis y limpieza de valores nulos,
se completaron datos faltantes, se eliminaron algunas columnas y se cambiaron el nombre de otras, se transformaron los tipos de datos, etc. 

> Para ver en detalle las tareas realizadas en esta etapa, ingrese al siguiente link: [ETL](/ETL.ipynb)

### Feature Engineering
![Pandas](https://img.shields.io/badge/-Pandas-333333?style=flat&logo=pandas)
![Numpy](https://img.shields.io/badge/-Numpy-333333?style=flat&logo=numpy)
![VSCode](https://img.shields.io/badge/-VSCode-333333?style=flat&logo=visual-studio-code)
![Jupyter](https://img.shields.io/badge/-Jupyter-333333?style=flat&logo=jupyter)
![Python](https://img.shields.io/badge/-Python-333333?style=flat&logo=python)
![Beautiful Soup](https://img.shields.io/badge/Beautiful%20Soup-333333?style=flat&logo=beautiful)
![TextBlob](https://img.shields.io/badge/TextBlob-333333?style=flat&logo=textblob)

La ingeniería de características se centró en el análisis de sentimientos de los comentarios de los usuarios, usando la librería TextBlob. 

Además, se prepararon los conjuntos de datos necesarios para optimizar las consultas y funcionalidades del servicio en la nube.

### EDA (Exploratory Data Analysis)

Se llevó a cabo un análisis exploratorio de los tres conjuntos de datos después del proceso de ETL. Esto permitió visualizar mejor las variables categóricas y numéricas, identificando las que son esenciales para el modelo de recomendación.

### Desarrollo de la API

Se construyó una API mediante el uso del framework FastAPI. Esta API ofrece varias funciones, estas son: 

- **PlayTimeGenre:** Esta función recibe como parametro un genero de juego y retorna el año con más horas jugadas para ese genero.

- **UserForGenre:** Esta función recibe como parametro un genero de juego y retorna el usuario con más horas jugadas para dicho genero, y una lista de aculuación de horas jugadas para dicho genero.

- **UsersRecommend:** Esta función recibe como parametro un año y retorna el top 3 de los juegos más recomendados para dicho año.

- **UsersNotRecommend:** Esta función recibe como parametro un año y retorna el top 3 de los juegos menos recomendados para dicho año.

- **SentimentAnalysis:** Esta función recibe como parametro un año y retorna una lista con la cantidad de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento.

- **GameRecommendation:** Esta función recibe como parametro el id de un juego y retorna una lista de los 5 juegos recomendados similares al ingreso.

### Modelamiento (Desarrollo de modelos de aprendizaje automático)

Para el desarrollo del Sistema de Recomendación, usamos el dataset resultante de etapas anteriores y creamos otro que contiene:

- **id**: ID del juego.
- **app_name**: Nombre del juego.
- **tags**: Etiquetas del juego.


### Despliegue

La API se desplegó en Render.com y está disponible en [https://deploy-p1-milagros.onrender.com/docs](https://deploy-p1-milagros.onrender.com/docs).

