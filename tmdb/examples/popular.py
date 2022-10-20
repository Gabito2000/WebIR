from tmdbv3api import TMDb, Movie
from decouple import config

tmdb = TMDb()

tmdb.api_key = config('TMDB_API_KEY')

movie = Movie()

popular = movie.popular()

for p in popular:
    print(p.title)
    print(p.overview)
