import pymongo 
from pymongo import MongoClient
from recommendations import *



# crea una instancia de conexión con la base de datos MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")

# selecciona la base de datos que quieres usar
db = client.knoxquack

collection = db.games

collection = db.users

# haz una consulta a la colección de games para obtener los primeros 5 juegos

# Carga del sistema de Recomendación 

# Cargamos la sesión de spark
rec_system = RecommendationSystem()
# Cargamos el modelo
model = rec_system.loadAlsModel()
# Cargamos los datos para mostrar los juegos posteriormente
games_names = rec_system.loadGamesNames()
# Cargamos los juegos más votados para pasarle al modelo
popular_games = rec_system.loadPopularGames()



def show_all_games(): 
    juegos = db.games.find()
    return juegos


def show_limit(limit:int):
    resultados = db.games.find().limit(limit)
    return resultados



def collection():
    collection = db.games 
    return collection 

def users_list():
    users = db.users.distinct("username")
    return users

def find_user(query):
    query = {"username" : query}
    user_query = db.users.find_one(query)
    if user_query:
        return user_query
    else:
        return None 
    

def show_user_reviews(userid):
    user_reviews = db.users.aggregate(
        [
            {
                "$match": {
                "user_id": userid
                }
            },
            {
                "$lookup": {
                "from": "reviews",
                "localField": "user_id",
                "foreignField": "user_id",
                "as": "user_reviews"
                }
            },
            {
                "$unwind": "$user_reviews"
            },
            {
                "$lookup": {
                "from": "games",
                "localField": "user_reviews.game_id",
                "foreignField": "game_id",
                "as": "user_game_reviews"
                }
            }, 
            {
                "$unwind": "$user_game_reviews"
            },
            {
                "$project": {
                "username": "$user_reviews.username",
                "game_id": "$user_reviews.game_id",
                "game_title": "$user_game_reviews.title",
                "user_score": "$user_reviews.score",
                "user_review_date": "$user_reviews.review_date"
                }
            }
                   
        ]
    )

    if user_reviews:
        return user_reviews
    else:
        return None
    

def get_recommendations(userid):
    fitted_data = rec_system.makePrediction(popular_games, userid)
    recommendations = model.transform(fitted_data)
    final_recs = rec_system.transformDataOutput(recommendations, games_names)
    return final_recs