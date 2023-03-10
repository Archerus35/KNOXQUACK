#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 14:03:45 2023

@author: yellowflash
"""

import findspark 
from pyspark.sql import SparkSession 
from pyspark.ml.recommendation import ALSModel
from pyspark.sql.functions import col,lit
from dataclasses import dataclass

def make_recommendations(userid):
    findspark.init()
    
    spark = SparkSession.builder.getOrCreate()
    
    model = ALSModel.load('als_model')
    
    popularGames = spark.read.option("header", "true").csv('popular_games.csv') 
    
    #popularGames.show()
    
    popularGames = popularGames.withColumn("game_id", col("game_id").cast("int"))
    popularGames = popularGames.withColumn("count", col("count").cast("int"))
    
    #popularGames.printSchema()
    
    
    userPopular = popularGames.select("game_id").withColumn("user_id", lit(userid))
    
    
    
    recommendations = model.transform(userPopular)
    
    topRecommendations = recommendations.sort(recommendations.prediction.desc()).take(20)
    
    #recommendations.show()
    df_recommendations = spark.createDataFrame(topRecommendations).toPandas()
    
    
    return df_recommendations



class RecommendationSystem:
    
    def __init__(self):
        findspark.init()
        self.spark = SparkSession.builder.getOrCreate()
        
       
    def stop_spark(self):
        self.spark.stop()
        
       
    def loadGamesNames(self):
        gamesNames = {}
        df_games = self.spark.read.json('./metacritic_scrape/games.json') 
        df_games = df_games.toPandas()
        columns = ['game_id', 'title', 'img_url']
        games_data =df_games[columns].values
        for game in games_data:
            gamesNames[game[0]] = tuple(game[1:])
        return gamesNames
        
    
    def loadAlsModel(self):
        model = ALSModel.load('als_model')
        return model
    
    def loadPopularGames(self):
        popularGames = self.spark.read.option("header", "true").csv('popular_games.csv') 
        popularGames = popularGames.withColumn("game_id", col("game_id").cast("int"))
        popularGames = popularGames.withColumn("count", col("count").cast("int"))
        return popularGames
    
    def makePrediction(self, popularGames, userid):
        userPopular = popularGames.select("game_id").withColumn("user_id", lit(userid))
        return userPopular
    
    
    def transformDataOutput(self, recommendations, games_names): 
        final_recs = []
        topRecommendations = recommendations.sort(recommendations.prediction.desc()).take(20)
        for rec in topRecommendations:
            game_id = rec['game_id']
            game_title = games_names[rec['game_id']][0]
            img_url = games_names[rec['game_id']][1]
            affinity = rec['prediction']
            rec_data = {
                    "game_id": game_id, 
                    "game_title": game_title,
                    "img_url":img_url,
                    "affinity": affinity,
                }
            final_recs.append(rec_data)
        return final_recs
        
    
    


rec_system = RecommendationSystem() 

model = rec_system.loadAlsModel()

games = rec_system.loadGamesNames()

pop = rec_system.loadPopularGames()

pred = rec_system.makePrediction(pop, 9996942)

predictions = model.transform(pred)

final_recs = rec_system.transformDataOutput(predictions, games)

print(final_recs[0])

        
        
        
        
        
        
        
        
        
        