import streamlit as st
import pymongo
from pymongo import MongoClient
import streamlit as st
import pandas as pd
import numpy as np




# crea una instancia de conexión con la base de datos MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")

# selecciona la base de datos que quieres usar
db = client.knoxquack

collection = db.games

# haz una consulta a la colección de games para obtener los primeros 5 juegos
resultados = db.games.find().limit(5)

# muestra los resultados en una tabla de Streamlit
#st.write("Los primeros 5 juegos:")
#for resultado in resultados:
    #st.write(resultado)

titles = pd.DataFrame(collection.distinct("title")[:6], columns=["Titulo"])
#description = pd.DataFrame(collection.distinct("description")[:11], columns=["description"])
score = pd.DataFrame(collection.distinct("score")[:6], columns=["Puntuacion"])
date = pd.DataFrame(collection.distinct("date")[:6], columns=["Fecha"])
#img_url = pd.DataFrame(collection.distinct("img_url")[:6], columns=["Imagen"])
tablas = pd.concat([titles,score,date],axis=1)
st.table(tablas)

game_titles = collection.distinct("title")
game_title = st.selectbox("Seleccionar un juego:", game_titles)

# Retrieve data for game title from MongoDB
if game_title:
    query = {"title": game_title}
    data = collection.find_one(query)
    if data:
        title = data["title"]
        score = data["score"]
        date = data["date"]
        
        # Create DataFrame and display as table
        df = pd.DataFrame({"Titulo": [title], "Puntuacion": [score], "Fecha": [date]})
        st.table(df)
    else:
        st.write("No hay datos sobre ese juego:", game_title)


