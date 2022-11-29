from math import pow, sqrt
import sqlite3
import pandas as pd
import random
import threading

conn = sqlite3.connect(
    'C:/Users/gabri/Desktop/Faculta/WebIR/WebIR/WebIR/GeneradorDeEstructuras/dataBase/Peliculas.db')
ratings = pd.read_sql_query("SELECT * from UsuariosPeliculas", conn)
movies = pd.read_sql_query("SELECT * from Peliculas", conn)
distributors = pd.read_sql_query("SELECT * from PeliculasDistibuidores", conn)
indiceInvertidoPelicualsUsuario = pd.read_sql_query("SELECT * from IndiceInvertidoPeliculasUsuarios", conn)

def get_usuarios_from_pelicula(pelicula):
    # c = conn.cursor()
    # c.execute('SELECT * FROM IndiceInvertidoPeliculasUsuarios WHERE idPelicula = ?', (pelicula,))
    # indiceInvertidoPeliculasUsuarios = c.fetchone()

    indiceInvertidoPeliculasUsuarios = indiceInvertidoPelicualsUsuario.loc[indiceInvertidoPelicualsUsuario.idPelicula == pelicula, 'idUsuarios'].tolist()
    if indiceInvertidoPeliculasUsuarios.__len__() == 0:
        print("No hay usuarios que hayan visto esta pelicula "+ str(pelicula))
        return []
    return indiceInvertidoPeliculasUsuarios[0].split(',')

def get_rating_(userid, movieid):
    return (ratings.loc[(ratings.idUsuario == userid) & (ratings.idPelicula == movieid), 'calification'].iloc[0])

def get_movieids_(userid):
    return ratings.loc[(ratings.idUsuario == userid), 'idPelicula'].tolist()

def get_movieids_calification_(userid):
    return ratings.loc[(ratings.idUsuario == userid), ['idPelicula','calification']]


def get_movie_title_(movieid):
    return (movies.loc[(movies.id == movieid), 'title'].iloc[0])

def get_movie_distributors_(movieid):
    return (distributors.loc[(distributors.id == movieid), 'distributors'].tolist()[0].split(','))

def distance_similarity_score(user1, user2):
    '''
    user1 & user2 : user ids of two users between which similarity        score is to be calculated.
    '''
    both_watch_count = 0
    for element in user1:
        if element in ratings.loc[ratings.idUsuario == user2, 'idPelicula'].tolist():
            both_watch_count += 1
    if both_watch_count == 0:
        return 0

    distance = []
    for element in user1:
        if element in ratings.loc[ratings.idUsuario == user2, 'idPelicula'].tolist():
            rating1 = user1[1]
            rating2 = get_rating_(user2, element)
            distance.append(pow(rating1 - rating2, 2))
    total_distance = sum(distance)

    return 1/(1+sqrt(total_distance))


def pearson_correlation_score(user1, user2):
    '''
    user1 & user2 : user ids of two users between which similarity score is to be calculated.
    '''
    both_watch_count = []

    for element in user1:
        if element[0] in ratings.loc[ratings.idUsuario == user2, 'idPelicula'].tolist():
            both_watch_count.append(element[0])
    
    if len(both_watch_count) == 0:
        return 0
    rating_sum_1 = sum([element[1] for element in user1 if element[0] in both_watch_count])
    rating_sum_2 = sum([get_rating_(user2, element) for element in both_watch_count])
    rating_squared_sum_1 = sum(
        [pow(element[1], 2) for element in user1 if element[0] in both_watch_count])
    rating_squared_sum_2 = sum(
        [pow(get_rating_(user2, element), 2) for element in both_watch_count])
    product_sum_rating = sum([element[1] * get_rating_(user2, element[0]) for element in user1 if element[0] in both_watch_count])
    
    numerator = product_sum_rating - ((rating_sum_1 * rating_sum_2) / len(both_watch_count))
    denominator = sqrt((rating_squared_sum_1 - pow(rating_sum_1,2) / len(both_watch_count)) * (rating_squared_sum_2 - pow(rating_sum_2,2) / len(both_watch_count)))
    if denominator == 0:
        return 0
    return numerator/denominator


def most_similar_users_(user1, number_of_users, metric='pearson'):
    '''
    user1 : Targeted User
    number_of_users : number of most similar users you want to user1.
    metric : metric to be used to calculate inter-user similarity score. ('pearson' or else)
    '''
    
    # user_ids = ratings.idUsuario.unique().tolist()

    # get all users from the movies that user1 has watched
    #set of users id
    user_ids = set()
    for elements in user1:
        movie = elements[0]
        #append if not repited
        for user in get_usuarios_from_pelicula(movie):
            user_ids.add(int(user))

    similarity_score = []
    if (metric == 'pearson'):
        similarity_score = [(pearson_correlation_score(user1, nth_user), nth_user)
                            for nth_user in user_ids]
    else:
        similarity_score = [(distance_similarity_score(user1, nth_user), nth_user)
                            for nth_user in user_ids]
    similarity_score.sort()
    similarity_score.reverse()
    similar_users = []
    i = 0
    while i < len(similarity_score) and (len(similar_users) < number_of_users or similarity_score[i][0] > 0.9):
        if similarity_score[i][0] != 1:
            similar_users.append(similarity_score[i])
        i = i+1

    return similar_users

def recommend_movies(user, streaming_services, max):
    if len(user) < 5:
        return random_titles(20)
    similar = []
    similar = most_similar_users_(user, 10)
    print(similar)
    if similar == [] or similar[0][0] == 0:
        print("No hay usuarios similares")
        return random_titles(20)
    viewedMoviesUser = [element[0] for element in user]
    notViewedMovies = {}
    notViewedWeight = []
    def get_movies(u):
        ratingsBd = get_movieids_calification_(u[1])
        movies = ratingsBd.idPelicula.tolist()
        for m in movies:
            if m not in viewedMoviesUser:
                movieDistributors = get_movie_distributors_(m)
                if (m in notViewedMovies or any(item in movieDistributors for item in streaming_services)):
                    if m not in notViewedMovies:
                        notViewedMovies[m] = (ratingsBd.loc[ratingsBd.idPelicula == m, 'calification'].iloc[0] * u[0], 1)
                    else:
                        (r, c) = notViewedMovies[m]
                        (auxr, auxc) = (r + get_rating_(u[1], m)*u[0], c+1)
                        notViewedMovies[m] = (auxr, auxc)
    threds = []
    for u in similar:
        threds.append(threading.Thread(target=get_movies, args=(u,)))
    for t in threds:
        t.start()
    for t in threds:
        t.join()
    

    for m in notViewedMovies:
        (r, c) = notViewedMovies[m]
        weight = round(r/c)
        notViewedWeight.append((m, weight))
    sortedMovies = sorted(notViewedWeight, key=lambda x: x[1], reverse=True)
    print("returnTitles", sortedMovies[:max])
    return sortedMovies[:max]

def random_titles(max):
    ran = random.choices(movies["id"], k=max)
    return [(r, 0) for r in ran]