from math import pow, sqrt
from IndiceInvertidoPeliculasUsuarios import *


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
        if element in ratings.loc[ratings.idUsuario == user2, 'idPelicula'].tolist():
            both_watch_count.append(element)

    if len(both_watch_count) == 0:
        return 0

    rating_sum_1 = sum([element[1] for element in user1 if element[0] in both_watch_count])
    rating_sum_2 = sum([get_rating_(user2, element)
                       for element in both_watch_count])
    rating_squared_sum_1 = sum(
        [pow(element[1]) for element in user1 if element[0] in both_watch_count])
    rating_squared_sum_2 = sum(
        [pow(get_rating_(user2, element), 2) for element in both_watch_count])
    product_sum_rating = sum([element[1] * get_rating_(user2, element[0]) for element in user1 if element[0] in both_watch_count])

    numerator = product_sum_rating - \
        ((rating_sum_1 * rating_sum_2) / len(both_watch_count))
    denominator = sqrt((rating_squared_sum_1 - pow(rating_sum_1, 2) / len(both_watch_count))
                       * (rating_squared_sum_2 - pow(rating_sum_2, 2) / len(both_watch_count)))

    if denominator == 0:
        return 0
    return numerator/denominator


def most_similar_users_(user1, number_of_users, metric='pearson'):
    '''
    user1 : Targeted User
    number_of_users : number of most similar users you want to user1.
    metric : metric to be used to calculate inter-user similarity score. ('pearson' or else)
    '''
    user_ids = ratings.idUsuario.unique().tolist()

    if (metric == 'pearson'):
        similarity_score = [(pearson_correlation_score(user1, nth_user), nth_user)
                            for nth_user in user_ids[:100] if nth_user != user1]
    else:
        similarity_score = [(distance_similarity_score(user1, nth_user), nth_user)
                            for nth_user in user_ids[:100] if nth_user != user1]

    similarity_score.sort()
    similarity_score.reverse()
    similar_users = []
    i = 0
    while len(similar_users) < number_of_users or similarity_score[i][0] > 0.9 and i < len(similarity_score):
        if similarity_score[i][0] != 1:
            similar_users.append(similarity_score[i])
        i = i+1
    return similar_users


def recommend_movies(user, streaming_services, max):
    similar = most_similar_users_(user, 10)
    viewedMoviesUser = [element[0] for element in user]
    notViewedMovies = {}
    notViewedWeight = []
    for u in similar:
        movies = get_movieids_(u[1])
        for m in movies:
            if m not in viewedMoviesUser and any(item in get_movie_distributors_(get_movie_title_(m)) for item in streaming_services):
                if m not in notViewedMovies:
                    notViewedMovies[m] = (get_rating_(u[1], m)*u[0], 1)
                else:
                    (r, c) = notViewedMovies[m]
                    (auxr, auxc) = (r + get_rating_(u[1], m)*u[0], c+1)
                    notViewedMovies[m] = (auxr, auxc)
    for m in notViewedMovies:
        (r, c) = notViewedMovies[m]
        weight = round(r/c)
        notViewedWeight.append((m, weight))
    sortedMovies = sorted(notViewedWeight, key=lambda x: x[1], reverse=True)
    returnTitles = []
    for (m, r) in sortedMovies[:max]:
        returnTitles.append(get_movie_title_(m))
    return returnTitles
