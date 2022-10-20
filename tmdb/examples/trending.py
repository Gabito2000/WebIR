from tmdbv3api import TMDb, Trending
from decouple import config

tmdb = TMDb()

tmdb.api_key = config('TMDB_API_KEY')

trending = Trending()

# What are the TV shows trending today?
shows= trending.tv_day()

for p in shows:
    print(p.name)
    print(p.overview)

# What are the Movies trending this week?
movies = trending.movie_week()

for p in movies:
    print(p.name)
    print(p.overview)
