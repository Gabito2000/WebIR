from tmdbv3api import TMDb, Genre
from decouple import config

tmdb = TMDb()

tmdb.api_key = config('TMDB_API_KEY')
tmdb.debug = True

genre = Genre()

genres = genre.movie_list()

for g in genres:
    print(g.id)
    print(g.name)
