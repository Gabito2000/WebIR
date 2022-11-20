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

# connect to the database
conn = sqlite3.connect('/dataBase/Peliculas.db')
c = conn.cursor()

# get the usuarios peliculas
c.execute('SELECT * FROM UsuariosPeliculas')
usuariosPeliculas = c.fetchall()

# creates the table for the inverted index idPelicula, list of idUsuarios idPelicula is a foreing key to Peliculas
c.execute('DROP TABLE IF EXISTS IndiceInvertidoPeliculasUsuarios')
c.execute('CREATE TABLE IndiceInvertidoPeliculasUsuarios (idPelicula integer primary key, idUsuarios text) FOREIGN KEY(idPelicula) REFERENCES Peliculas(idPelicula)')
#c.execute('CREATE TABLE IndiceInvertidoPeliculasUsuarios (idPelicula INTEGER PRIMARY KEY, idUsuarios TEXT)')
conn.commit()

# adds the data to the table
for usuarioPelicula in usuariosPeliculas:
    idUsuario = usuarioPelicula[0]
    idPelicula = usuarioPelicula[1]
    c.execute('SELECT * FROM IndiceInvertidoPeliculasUsuarios WHERE idPelicula = ?', (idPelicula,))
    indiceInvertidoPeliculasUsuarios = c.fetchone()
    if indiceInvertidoPeliculasUsuarios is None:
        c.execute('INSERT INTO IndiceInvertidoPeliculasUsuarios VALUES (?, ?)', (idPelicula, str(idUsuario)))
    else:
        idUsuarios = indiceInvertidoPeliculasUsuarios[1]
        idUsuarios = idUsuarios + ',' + str(idUsuario)
        c.execute('UPDATE IndiceInvertidoPeliculasUsuarios SET idUsuarios = ? WHERE idPelicula = ?', (idUsuarios, idPelicula))
    conn.commit()


# get the usuario FROM a pelicula in usuarios peliculas
def getUsuarioFromPelicula(idPelicula):
    c.execute('SELECT * FROM IndiceInvertidoPeliculasUsuarios WHERE idPelicula = ?', (idPelicula,))
    indiceInvertidoPeliculasUsuarios = c.fetchone()
    if indiceInvertidoPeliculasUsuarios is None:
        return None
    else:
        idUsuarios = indiceInvertidoPeliculasUsuarios[1]
        idUsuarios = idUsuarios.split(',')
        return idUsuarios






