# inport for a sql database two tables Usuarios and Peliculas
# and a table with the relation between the two tables
# the table is called UsuariosPeliculas
# the table UsuariosPeliculas has the following columns
# idUsuario, idPelicula, calificacion
# the table Usuarios has the following columns
# idUsuario
# the table Peliculas has the following columns
# idPelicula, titulo

import sqlite3
import sys
import pandas as pd

# # connect to the database
# conn = sqlite3.connect('/dataBase/Peliculas.db')
# c = conn.cursor()

# # get the usuarios peliculas
# c.execute('SELECT * FROM UsuariosPeliculas')
# usuariosPeliculas = c.fetchall()

# # creates the table for the inverted index idPelicula, list of idUsuarios idPelicula is a foreing key to Peliculas
# c.execute('DROP TABLE IF EXISTS IndiceInvertidoPeliculasUsuarios')
# c.execute('CREATE TABLE IndiceInvertidoPeliculasUsuarios (idPelicula integer primary key, idUsuarios text) FOREIGN KEY(idPelicula) REFERENCES Peliculas(idPelicula)')
# #c.execute('CREATE TABLE IndiceInvertidoPeliculasUsuarios (idPelicula INTEGER PRIMARY KEY, idUsuarios TEXT)')
# conn.commit()

# # adds the data to the table
# for usuarioPelicula in usuariosPeliculas:
#     idUsuario = usuarioPelicula[0]
#     idPelicula = usuarioPelicula[1]
#     c.execute(
#         'SELECT * FROM IndiceInvertidoPeliculasUsuarios WHERE idPelicula = ?', (idPelicula,))
#     indiceInvertidoPeliculasUsuarios = c.fetchone()
#     if indiceInvertidoPeliculasUsuarios is None:
#         c.execute('INSERT INTO IndiceInvertidoPeliculasUsuarios VALUES (?, ?)',
#                   (idPelicula, str(idUsuario)))
#     else:
#         idUsuarios = indiceInvertidoPeliculasUsuarios[1]
#         idUsuarios = idUsuarios + ',' + str(idUsuario)
#         c.execute('UPDATE IndiceInvertidoPeliculasUsuarios SET idUsuarios = ? WHERE idPelicula = ?',
#                   (idUsuarios, idPelicula))
#     conn.commit()


# # get the usuario FROM a pelicula in usuarios peliculas
# def getUsuarioFromPelicula(idPelicula):
#     c.execute(
#         'SELECT * FROM IndiceInvertidoPeliculasUsuarios WHERE idPelicula = ?', (idPelicula,))
#     indiceInvertidoPeliculasUsuarios = c.fetchone()
#     if indiceInvertidoPeliculasUsuarios is None:
#         return None
#     else:
#         idUsuarios = indiceInvertidoPeliculasUsuarios[1]
#         idUsuarios = idUsuarios.split(',')
#         return idUsuarios


conn = sqlite3.connect(
    'C:/Users/gabri/Desktop/Faculta/WebIR/WebIR/WebIR/GeneradorDeEstructuras/dataBase/Peliculas.db')
ratings = pd.read_sql_query("SELECT * from UsuariosPeliculas", conn)
movies = pd.read_sql_query("SELECT * from Peliculas", conn)
distributors = pd.read_sql_query("SELECT * from PeliculasDistibuidores", conn)


def get_rating_(userid, movieid):
    return (ratings.loc[(ratings.idUsuario == userid) & (ratings.idPelicula == movieid), 'calification'].iloc[0])


def get_movieids_(userid):
    return (ratings.loc[(ratings.idUsuario == userid), 'idPelicula'].tolist())


def get_movie_title_(movieid):
    return (movies.loc[(movies.id == movieid), 'title'].iloc[0])


def get_movie_distributors_(movieid):
    return (distributors.loc[(distributors.title == movieid), 'distributors'].tolist()[0].split(','))
