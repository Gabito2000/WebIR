# backend that gets a list of movies objects as a post request and returns a list of movies objects as a response fastapi

import sys
from fastapi import FastAPI
from typing import List, Union
from pydantic import BaseModel

sys.path.append('/Users/tali/Desktop/WebIR/GeneradorDeEstructuras')

from GeneradorDeEstructuras.pruebaUsandoEstructuras import recommend_movies

app = FastAPI()
 

class Movie(BaseModel):
    id: int
    stars: int


@app.post("/movies")
async def create_movie(movies: List[Movie], distribuidores: List[int]):
    user = []
    distributors = []
    for movie in movies:
        user.append((movie.id, movie.stars))
    for d in distribuidores:
        distributors.append(str(d))
    return recommend_movies(user, distributors, 10)
