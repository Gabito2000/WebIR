from tmdbv3api import TMDb, Search
from decouple import config

tmdb = TMDb()

tmdb.api_key = config('TMDB_API_KEY')

search = Search()

results = search.movies({"query": "Matrix", "year": 1999})

for result in results:
    print(result.title)
    print(result.overview)
