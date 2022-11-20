# import for a sql database two tables Usuarios and Peliculas
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
conn = sqlite3.connect('./dataBase/Peliculas.db')
c = conn.cursor()

# get all perliculas valued by a user in usuarios peliculas 
def getPeliculasFromUsuarios(idUsuario):
    c.execute('SELECT * FROM UsuariosPeliculas WHERE idUsuario = ?', (idUsuario,))
    usuariosPeliculas = c.fetchall()
    if usuariosPeliculas is None:
        return None
    else:
        return usuariosPeliculas


# get a map of peliculas from a list of usuarios with idUsuario as Key
def getPeliculasUsuariosFromUsuariosList(idUsuarios):
    peliculasUsuarios = {}
    for idUsuario in idUsuarios:
        peliculasUsuario = getPeliculasFromUsuarios(idUsuario)
        peliculasUsuarios[idUsuario] = peliculasUsuario
    return peliculasUsuarios