from tmdbv3api import TMDb, Search
from decouple import config

tmdb = TMDb()

tmdb.api_key = config('TMDB_API_KEY')

search = Search()

results = search.multi({"query": "Will", "page": 1})

for result in results:
    print(result.media_type)
