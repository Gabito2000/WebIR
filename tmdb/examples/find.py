from tmdbv3api import TMDb, Find
from decouple import config

tmdb = TMDb()

tmdb.api_key = config('TMDB_API_KEY')

find = Find()

results = find.find_by_imdb_id("tt0076759")

for r in results["movie_results"]:
    print(r.title)
    print(r.id)
    
results = find.find_by_tvdb_id("83268")

for r in results["tv_results"]:
    print(r.title)
    print(r.id)

results = find.find("tt0076759", "imdb_id")

for r in results["movie_results"]:
    print(r.title)
    print(r.id)
    