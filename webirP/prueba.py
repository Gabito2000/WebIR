import pandas as panda
from math import pow, sqrt

r_cols = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings = panda.read_csv('data/ratings.csv',
                        header=0, #skiprows=1
                        names=r_cols,
                        encoding='latin-1')

user_ids = ratings.user_id.unique().tolist()
movie_ids = ratings.movie_id.unique().tolist()
#print('Number of Users: {}'.format(len(user_ids)))
#print('Number of Movies: {}'.format(len(movie_ids)))

#print(format(ratings))

m_cols = ['movie_id', 'movie_title', 'genre']
movies = panda.read_csv('data/movies.csv', header=0, names=m_cols, encoding='latin-1')
#print('movies: {}'.format(movies))

# Getting series of lists by applying split operation.
movies.genre = movies.genre.str.split('|')
# Getting distinct genre types for generating columns of genre type.
genre_columns = list(set([j for i in movies['genre'].tolist() for j in i]))
# Iterating over every list to create and fill values into columns.
for j in genre_columns:
    movies[j] = 0
for i in range(movies.shape[0]):
    for j in genre_columns:
        if(j in movies['genre'].iloc[i]):
            movies.loc[i,j] = 1
# Separting movie title and year part using split function.
split_values = movies['movie_title'].str.split("(", n = 1, expand = True)
# setting 'movie_title' values to title part.
movies.movie_title = split_values[0]
# creating 'release_year' column.
movies['release_year'] = split_values[1]
# Cleaning the release_year series.
movies['release_year'] = movies.release_year.str.replace(')','')
# dropping 'genre' columns as it has already been one hot encoded.
movies.drop('genre',axis=1,inplace=True)

#print(format(movies))

def get_rating_(userid,movieid):
    return (ratings.loc[(ratings.user_id==userid) & (ratings.movie_id == movieid),'rating'].iloc[0])
def get_movieids_(userid):
    return (ratings.loc[(ratings.user_id==userid),'movie_id'].tolist())
def get_movie_title_(movieid):
    return (movies.loc[(movies.movie_id == movieid),'movie_title'].iloc[0])

def distance_similarity_score(user1,user2):
    '''
    user1 & user2 : user ids of two users between which similarity        score is to be calculated.
    '''
    both_watch_count = 0
    for element in ratings.loc[ratings.user_id==user1,'movie_id'].tolist():
        if element in ratings.loc[ratings.user_id==user2,'movie_id'].tolist():
            both_watch_count += 1
    if both_watch_count == 0 :
        return 0
    
    distance = []
    for element in ratings.loc[ratings.user_id==user1,'movie_id'].tolist():
        if element in ratings.loc[ratings.user_id==user2,'movie_id'].tolist():
            rating1 = get_rating_(user1,element)
            rating2 = get_rating_(user2,element)
            distance.append(pow(rating1 - rating2, 2))
    total_distance = sum(distance)
    
    return 1/(1+sqrt(total_distance))

def pearson_correlation_score(user1,user2):
    '''
    user1 & user2 : user ids of two users between which similarity score is to be calculated.
    '''
    both_watch_count = []
    
    for element in ratings.loc[ratings.user_id==user1,'movie_id'].tolist():
        if element in ratings.loc[ratings.user_id==user2,'movie_id'].tolist():
            both_watch_count.append(element)
    
    if len(both_watch_count) == 0 :
        return 0
    
    rating_sum_1 = sum([get_rating_(user1,element) for element in both_watch_count])
    rating_sum_2 = sum([get_rating_(user2,element) for element in both_watch_count])
    rating_squared_sum_1 = sum([pow(get_rating_(user1,element),2) for element in both_watch_count])
    rating_squared_sum_2 = sum([pow(get_rating_(user2,element),2) for element in both_watch_count])
    product_sum_rating = sum([get_rating_(user1,element) * get_rating_(user2,element) for element in both_watch_count])
    
    numerator = product_sum_rating - ((rating_sum_1 * rating_sum_2) / len(both_watch_count))
    denominator = sqrt((rating_squared_sum_1 - pow(rating_sum_1,2) / len(both_watch_count)) * (rating_squared_sum_2 - pow(rating_sum_2,2) / len(both_watch_count)))
    
    if denominator == 0:
        return 0
    return numerator/denominator

def most_similar_users_(user1,number_of_users,metric='pearson'):
    '''
    user1 : Targeted User
    number_of_users : number of most similar users you want to user1.
    metric : metric to be used to calculate inter-user similarity score. ('pearson' or else)
    '''
    user_ids = ratings.user_id.unique().tolist()
    
    if(metric == 'pearson'):
        similarity_score = [(pearson_correlation_score(user1,nth_user),nth_user) for nth_user in user_ids[:100] if nth_user != user1]
    else:
        similarity_score = [(distance_similarity_score(user1,nth_user),nth_user) for nth_user in user_ids[:100] if nth_user != user1]
    
    similarity_score.sort()
    similarity_score.reverse()
    
    return similarity_score[:number_of_users]
print(most_similar_users_(1,10))