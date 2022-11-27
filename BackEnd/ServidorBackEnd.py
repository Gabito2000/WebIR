# backend that gets a list of movies objects as a post request and returns a list of movies objects as a response fastapi
import os
import sys
sys.path.append('../GeneradorDeEstructuras')
from fastapi import FastAPI
from typing import List, Union
from pydantic import BaseModel
import requests
import threading
import sqlite3
import pandas as pd

from pruebaUsandoEstructuras import recommend_movies
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
BDPath = 'C:/Users/gabri/Desktop/Faculta/WebIR/WebIR/WebIR/GeneradorDeEstructuras/dataBase/Peliculas.db'
origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 

class Movie(BaseModel):
    id: int
    stars: int


@app.post("/movies")
async def create_movie(movies: List[Movie], distribuidores: List[str]):
    user = []
    distributors = []

    for movie in movies:
        #search in sqlite3 database for the movie with the id_imdb = movie.id
        conn = sqlite3.connect(BDPath)
        movies = pd.read_sql_query("SELECT * from Peliculas", conn)
        movie_bd = movies.loc[movies.id_imdb == movie.id]
        if len(movie_bd) > 0:
            movie_bd = movie_bd.iloc[0]
            user.append((movie_bd.id, movie.stars))
        else:
            print("movie not found")
    for d in distribuidores:
        distributors.append(d)
    recommend = recommend_movies(user, distributors, 10)
    #api post to imdb api to get the movies timeout 20 seconds
    movies = []
    
    def get_movies(movieName):
        querry = 'https://api.themoviedb.org/3/search/movie?api_key=f9a3efe8c813e81a40a9b661bde37457&query='+movieName.replace(" ","%20")
        response = requests.get(querry, timeout=20)
        if(response.status_code == 200):
            movies.append(response.json())
    def get_series(movieName):
        querry = 'https://api.themoviedb.org/3/search/tv?api_key=f9a3efe8c813e81a40a9b661bde37457&query='+movieName.replace(" ","%20")
        response = requests.get(querry, timeout=20)
        if(response.status_code == 200):
            movies.append(response.json())

    conn = sqlite3.connect(BDPath)
    titles = pd.read_sql_query("SELECT * from Titles", conn)
    threds = []
    for movieName in recommend:
        #get for the table titles if the movie is a movie or a serie
        title = titles.loc[titles.field2 == movieName]
        if len(title) > 0:
            title = title.iloc[0]
            if title.field4 == "MOVIE":
                threds.append(threading.Thread(target=get_movies, args=(movieName,)))
                print("movie "+ movieName)
            else:
                threds.append(threading.Thread(target=get_series, args=(movieName,)))
                print("serie "+ movieName)
    
    for t in threds:
        t.start()
    for t in threds:
        t.join()

    return movies

