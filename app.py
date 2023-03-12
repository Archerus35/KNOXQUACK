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

st.title("KnoxQuack")
st.subheader("Sistema de recomendación basado en puntuaciones")


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
    

    
   

tab1, tab2, tab3, tab4 = st.tabs(["Buscar Juegos :gamepad", "Ver Puntuaciones", "Chatbot", "Usuarios con más reviews"])

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
   
    user_reviews = show_user_reviews(user_data["user_id"])

    df_user_reviews = pd.DataFrame(list(user_reviews))
    columns = ['game_id', 'game_title', 'user_score', 'user_review_date']
    df_user_reviews_subset = df_user_reviews[columns]

    st.table(df_user_reviews_subset)

    st.subheader("Recomendaciones")

    recommendations = get_recommendations(user_data["user_id"])
    
    for rec in recommendations: 
        st.subheader(rec["game_title"])
        col1, col2 = st.columns(2)

        with col1: 
            st.image(rec["img_url"])
        with col2:
            st.caption("Afinidad")
            st.subheader(round(rec["affinity"],2))

with tab3:
    components.iframe("https://console.dialogflow.com/api-client/demo/embedded/90ff94ad-fac5-49f0-aabe-49237f6da2e6", height=430, width=350)   



with tab4:
    top_rating_users_data = pd.read_csv('./metacritic_scrape/top_rating_users.csv')
    st.table(top_rating_users_data)







     











