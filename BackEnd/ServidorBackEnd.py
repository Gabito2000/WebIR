#backend that gets a list of movies objects as a post request and returns a list of movies objects as a response fastapi

from fastapi import FastAPI
from typing import List, Union
from pydantic import BaseModel

app = FastAPI()

class Movie(BaseModel):
    id: int
    stars: int



@app.post("/movies")
async def create_movie(movies: List[Movie],distribuidores: List[int]):
    #poner logica de negocio acá 
    #llega una lista de objetos movie que tienen el id de la pelicula y las estrellas; y una lista de distribuidores que son los ids de los distribuidores
    return movies[0].id
