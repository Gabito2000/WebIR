import pandas as pd

# Obtenemos la info
column_names = ['user_id', 'item_id', 'rating', 'timestamp']
path = 'https://media.geeksforgeeks.org/wp-content/uploads/file.tsv'
df = pd.read_csv(path, sep='\t', names=column_names)

# Revisar la cabecera de los datos
df.head()

# Consulta todas las películas y sus respectivos ID
movie_titles = pd.read_csv('https://media.geeksforgeeks.org/wp-content/uploads/Movie_Id_Titles.csv')
movie_titles.head()

data = pd.merge(df, movie_titles, on='item_id')
data.head()

# Calcular la calificación media de todas las películas.
data.groupby('title')['rating'].mean().sort_values(ascending=True).head()

# Calcule la calificación de conteo de todas las películas.
data.groupby('title')['rating'].count().sort_values(ascending=True).head()

# Creamos un marco de datos con valores de conteo de 'calificación'
ratings = pd.DataFrame(data.groupby('title')['rating'].mean()) 
ratings['num of ratings'] = pd.DataFrame(data.groupby('title')['rating'].count())
ratings.head()

print(ratings)

#Para obtener el titulo de la pelicula
#for x in ratings.T:
#    print(x)

#Para obtener la calificacion de la pelicula
#for y in ratings.rating:
#    print(y)    

#Para obtener el numero de calificaciones de la pelicula
#for z in ratings['num of ratings']:
#    print(z)
