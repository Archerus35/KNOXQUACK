import streamlit as st
import pymongo
from pymongo import MongoClient
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

from controller import *


style = f'''
    <style>
        .appview-container .main .block-container {{
            max-width: 90%;
        }}
    </style>
  
  
  '''

st.markdown(style, unsafe_allow_html=True)

image = Image.open('image/pato.jpg')

st.image(image)


def display_game_card(game):
    st.subheader(str(game["game_id"]) + ". " +game["title"])
    subcol1, subcol2 = st.columns(2)
    
    with subcol1:
        st.image(game["img_url"])
        
    with subcol2:
        st.caption("Puntuación")
        st.subheader(game["score"]) 
        st.caption(game["date"])

    
   



# muestra los resultados en una tabla de Streamlit
#st.write("Los primeros 5 juegos:")
#for resultado in resultados:
    #st.write(resultado)
'''
titles = pd.DataFrame(collection.distinct("title")[:6], columns=["Titulo"])
#description = pd.DataFrame(collection.distinct("description")[:11], columns=["description"])
score = pd.DataFrame(collection.distinct("score")[:6], columns=["Puntuacion"])
date = pd.DataFrame(collection.distinct("date")[:6], columns=["Fecha"])
#img_url = pd.DataFrame(collection.distinct("img_url")[:6], columns=["Imagen"])
tablas = pd.concat([titles,score,date],axis=1)
st.table(tablas)

game_titles = collection.distinct("title")
game_title = st.selectbox("Seleccionar un juego:", game_titles)
'''

resultados = show_limit(5)
juegos = show_all_games()

primer_juego = resultados[0]
juego2 = resultados[1]
juego3 = resultados[2]
juego4 = resultados[3]
st.write(type(resultados))

st.write(len(list(juegos)))

col1, col2, col3, col4 = st.columns(4) 

with col1:
  display_game_card(primer_juego)
    
with col2:
  display_game_card(juego2)

with col3:
   display_game_card(juego3)

with col4: 
   display_game_card(juego4)







'''
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


'''
