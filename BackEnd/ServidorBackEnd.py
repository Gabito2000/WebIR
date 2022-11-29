# backend that gets a list of movies objects as a post request and returns a list of movies objects as a response fastapi
import os
import sys
sys.path.append('/Users/tali/Desktop/WebIR/GeneradorDeEstructuras')
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
BDPath = '/Users/tali/Desktop/WebIR/GeneradorDeEstructuras/dataBase/Peliculas.db'
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
    stars: float


@app.post("/movies")
async def create_movie(movies: List[Movie], distribuidores: List[str]):
    user = []
    distributors = []
    conn = sqlite3.connect(BDPath)
    moviesDB = pd.read_sql_query("SELECT * from Peliculas", conn)
    for movie in movies:
        #search in sqlite3 database for the movie with the id_imdb = movie.id
        
        movie_bd = moviesDB.loc[moviesDB.id_imdb == movie.id]
        if len(movie_bd) > 0:
            movie_bd = movie_bd.iloc[0]
            user.append((movie_bd.id, movie.stars))
        else:
            print("movie not found"+ str(movie.id))
    for d in distribuidores:
        distributors.append(d)
    recommend = recommend_movies(user, distributors, 10)
    #api post to imdb api to get the movies timeout 20 seconds
    movies = []
    def get_movies_by_id(id):
        url = 'https://api.themoviedb.org/3/movie/'+str(id)+'?api_key=f9a3efe8c813e81a40a9b661bde37457'
        response = requests.get(url)
        if response.status_code == 200:
            movies.append(response.json())
    def get_series_by_id(id):
        url = 'https://api.themoviedb.org/3/tv/'+str(id)+'?api_key=f9a3efe8c813e81a40a9b661bde37457'
        response = requests.get(url)
        if response.status_code == 200:
            movies.append(response.json())
    recommendIdImdb = []

    for (movieId, rating) in recommend:
        #search in sqlite3 database for the movie with the id_imdb = movie.id
        movie_bd = moviesDB.loc[moviesDB.id == movieId]
        if len(movie_bd) > 0:
            movie_bd = movie_bd.iloc[0]
            recommendIdImdb.append([movie_bd.id_imdb, movie_bd.id])

    conn = sqlite3.connect(BDPath)
    titles = pd.read_sql_query("SELECT * from titles", conn)
    threds = []
    for [movieId_IMDB, movieId] in recommendIdImdb:
        #get for the table titles if the movie is a movie or a serie
        title = titles.loc[titles.field1 == str(movieId)]
        #get the id from tmdb
        if len(title) > 0:
            title = title.iloc[0]
            if title.field4 == "MOVIE":
                threds.append(threading.Thread(target=get_movies_by_id, args=(movieId_IMDB,)))
            else:
                threds.append(threading.Thread(target=get_series_by_id, args=(movieId_IMDB,)))
        else:
            print("title not found "+ str(movieId))
    for t in threds:
        t.start()
    for t in threds:
        t.join()
    print("movies")
    print(movies)
    return movies   

