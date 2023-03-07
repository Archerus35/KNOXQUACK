import streamlit as st
import pymongo
from pymongo import MongoClient

# crea una instancia de conexión con la base de datos MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017")

# selecciona la base de datos que quieres usar
db = client.knoxquack

collection = db.games

# haz una consulta a la colección de games para obtener los primeros 5 juegos
resultados = collection.find().limit(5)

# muestra los resultados en una tabla de Streamlit
st.write("Los primeros 5 juegos:")
for resultado in resultados:
    st.write(resultado)