import pandas as pd

ratings = pd.read_csv('data/ratings.csv')
ratings.drop('timestamp', inplace=True, axis=1)
movies = pd.read_csv('data/movies.csv')
print(ratings)

ratings_entrada = [(1, '2.0'), (6, '5.0'), (32, '5.0'), (70, '1.0'), (170, '3.0'), (180, '1.0'), (231, '1.0'), (1001, '1.0'), (107565, '4.0')]

print(ratings[ratings.userId.isin([1])])
#get_users_that_saw_this_movie
#merge_all_users_and_the_ratings_for_the_chosen_movies
#pearson_correlation_between_the_ratings
#post_procesamiento_y_ranking_con_respecto_a_lo_que_el_usuario_tiene_acceso