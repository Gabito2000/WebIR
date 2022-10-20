from tmdbv3api import TMDb, TV
from decouple import config

tmdb = TMDb()

tmdb.api_key = config('TMDB_API_KEY')

tv = TV()

show = tv.search("Breaking Bad")

for result in show:
    print(result.name)
    print(result.overview)
