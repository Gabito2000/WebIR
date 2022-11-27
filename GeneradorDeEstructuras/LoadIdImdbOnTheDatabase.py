#loads all the database of peliculas and changes the id of all the peliculas to the id of imdb
#

import pandas as pd
import sqlite3
import requests
import threading
import time

conn = sqlite3.connect(
    'C:/Users/gabri/Desktop/Faculta/WebIR/WebIR/WebIR/GeneradorDeEstructuras/dataBase/Peliculas.db')
movies = pd.read_sql_query("SELECT * from Peliculas", conn)
movies = movies.drop_duplicates(subset=['title'])

def get_id_imdb(title):
    url = 'https://api.themoviedb.org/3/search/movie?api_key=f9a3efe8c813e81a40a9b661bde37457&query=' + title.replace(" ","%20")
    response = requests.get(url)
    if response.status_code == 200:
        if(len(response.json()['results']) > 0):
            return [response.json()['results'][0]['id'], response.json()['results'][0]['title']]
        return [None, None]
    else:
        return [None, None]


def get_id_imdb_thread(title):
    [id_imdb, title_imdb] = get_id_imdb(title)
    if id_imdb is not None:
        movies.loc[movies.title == title, 'id_imdb'] = id_imdb
        print(title + " " + str(id_imdb) + " " + str(title_imdb))
    else:
        print(title + " not found")

threads = []
for title in movies.title:
    t = threading.Thread(target=get_id_imdb_thread, args=(title,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

movies.to_sql('Peliculas', conn, if_exists='replace', index=False)
conn.close()