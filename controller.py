import pymongo 
from pymongo import MongoClient



# crea una instancia de conexión con la base de datos MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")

# selecciona la base de datos que quieres usar
db = client.knoxquack

collection = db.games

# haz una consulta a la colección de games para obtener los primeros 5 juegos



def show_all_games(): 
    juegos = db.games.find()
    return juegos


def show_limit(limit:int):
    resultados = db.games.find().limit(limit)
    return resultados