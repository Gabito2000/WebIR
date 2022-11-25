# backend that gets a list of movies objects as a post request and returns a list of movies objects as a response fastapi
import os
import sys
sys.path.append('../GeneradorDeEstructuras')
from fastapi import FastAPI
from typing import List, Union
from pydantic import BaseModel
import requests

from pruebaUsandoEstructuras import recommend_movies

app = FastAPI()
 

class Movie(BaseModel):
    id: int
    stars: int


@app.post("/movies")
async def create_movie(movies: List[Movie], distribuidores: List[str]):
    user = []
    distributors = []
    for movie in movies:
        user.append((movie.id, movie.stars))
    for d in distribuidores:
        distributors.append(d)
    recommend = recommend_movies(user, distributors, 10)
    #api post to imdb api to get the movies timeout 20 seconds
    movies = []
    for movieName in recommend:
        querry = 'https://api.themoviedb.org/3/search/movie?api_key=f9a3efe8c813e81a40a9b661bde37457&query="'+movieName+'"'
        response = requests.get(querry, timeout=20)
        if(response.status_code == 200):
            print(response.json())
            movies.append(response.json())
    return movies
    


