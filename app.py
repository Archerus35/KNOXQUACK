import streamlit as st
import pymongo
from pymongo import MongoClient
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import streamlit.components.v1 as components

from controller import *



resultados = show_limit(5) 
juegos = show_all_games()
usuarios = users_list()

collection = collection()



image = Image.open('image/pato.jpg')

st.image(image)


def display_game_card(game):
    st.subheader(str(game["game_id"]) + ". " +game["title"])
    subcol1, subcol2 = st.columns(2)
    
    with subcol1:
        st.image(game["img_url"])
               

    with subcol2:
        st.caption("Puntuación de la Crítica")
        st.subheader(game["score"]) 
        st.caption(game["date"])

    st.write(game["description"])
    

    
   

tab1, tab2, tab3 = st.tabs(["Buscar Juegos :gamepad", "Ver Puntuaciones", "Chatbot"])

with tab1: 
    
    # muestra los resultados en una tabla de Streamlit
    #st.write("Los primeros 5 juegos:")
    #for resultado in resultados:
    #st.write(resultado)
    game_titles = collection.distinct("title")
    game_title = st.selectbox("Seleccionar un juego:", game_titles)




   # Retrieve data for game title from MongoDB
    if game_title:
        query = {"title": game_title}
        data = collection.find_one(query)
        if data:
            display_game_card(data)
        else:
            st.write("No hay datos sobre ese juego:", game_title)

with tab2:
    users = users_list()
    select_users = st.selectbox("Seleccionar usuario", users)

    query = select_users
    user_data = find_user(query)
    if user_data:
        col1, col2 = st.columns(2)
        with col1:
            st.caption("Nombre de Usuario: ") 
            st.subheader(user_data["username"]) 
        with col2:
            st.caption("Id")
            st.subheader(user_data["user_id"])
    else:
        st.write("No existen datos de ese usuario")



    

with tab3:
    components.iframe("https://console.dialogflow.com/api-client/demo/embedded/90ff94ad-fac5-49f0-aabe-49237f6da2e6", height=430, width=350)   











     











