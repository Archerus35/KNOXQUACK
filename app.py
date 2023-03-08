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

titles = pd.DataFrame(collection.distinct("title")[:11], columns=["Titulo"])
#description = pd.DataFrame(collection.distinct("description")[:11], columns=["description"])
score = pd.DataFrame(collection.distinct("score")[:11], columns=["Puntuacion"])
date = pd.DataFrame(collection.distinct("date")[:11], columns=["Fecha"])
img_url = pd.DataFrame(collection.distinct("img_url")[:11], columns=["Imagen"])
tablas = pd.concat([titles,score,date,img_url],axis=1)
st.table(tablas)




