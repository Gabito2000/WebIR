from math import pow, sqrt
from IndiceInvertidoPeliculasUsuarios import *


def distance_similarity_score(user1, user2):
    '''
    user1 & user2 : user ids of two users between which similarity        score is to be calculated.
    '''
    both_watch_count = 0
    for element in ratings.loc[ratings.idUsuario == user1, 'idPelicula'].tolist():
        if element in ratings.loc[ratings.idUsuario == user2, 'idPelicula'].tolist():
            both_watch_count += 1
    if both_watch_count == 0:
        return 0

    distance = []
    for element in ratings.loc[ratings.idUsuario == user1, 'idPelicula'].tolist():
        if element in ratings.loc[ratings.idUsuario == user2, 'idPelicula'].tolist():
            rating1 = get_rating_(user1, element)
            rating2 = get_rating_(user2, element)
            distance.append(pow(rating1 - rating2, 2))
    total_distance = sum(distance)

    return 1/(1+sqrt(total_distance))


def pearson_correlation_score(user1, user2):
    '''
    user1 & user2 : user ids of two users between which similarity score is to be calculated.
    '''
    both_watch_count = []

    for element in ratings.loc[ratings.idUsuario == user1, 'idPelicula'].tolist():
        if element in ratings.loc[ratings.idUsuario == user2, 'idPelicula'].tolist():
            both_watch_count.append(element)

    if len(both_watch_count) == 0:
        return 0

    rating_sum_1 = sum([get_rating_(user1, element)
                       for element in both_watch_count])
    rating_sum_2 = sum([get_rating_(user2, element)
                       for element in both_watch_count])
    rating_squared_sum_1 = sum(
        [pow(get_rating_(user1, element), 2) for element in both_watch_count])
    rating_squared_sum_2 = sum(
        [pow(get_rating_(user2, element), 2) for element in both_watch_count])
    product_sum_rating = sum([get_rating_(
        user1, element) * get_rating_(user2, element) for element in both_watch_count])

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

    return similarity_score[:number_of_users]
