from tmdbv3api import TMDb, Movie
from decouple import config

tmdb = TMDb()
tmdb.api_key = config('TMDB_API_KEY')

movie = Movie()

m = movie.details(111)

print(m.title)
print(m.overview)
print(m.popularity)
