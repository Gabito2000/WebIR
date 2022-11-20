# import for a sql database two tables Distribuidores and Peliculas
# and a table with the relation between the two tables
# the table is called DistribuidoresPeliculas
# the table Distribuidores has the following columns
# idDistribuidores, tituloPelicula
# the table Distribuidores has the following columns
# idDistribuidores, nombreDistribuidor
# the table Peliculas has the following columns
# idPelicula, titulo

import sqlite3
import sys

# connect to the database
conn = sqlite3.connect('Peliculas.db')
c = conn.cursor()

# get DistribuidoresPeliculas
c.execute('SELECT * FROM DistribuidoresPeliculas')
distribuidoresPeliculas = c.fetchall()

# create the table
c.execute('DROP TABLE IF EXISTS DistribuidoresPeliculasIndiceInvertido')
c.execute('CREATE TABLE DistribuidoresPeliculasIndiceInvertido (idPelicula INTEGER PRIMARY KEY, distribuidores TEXT)')
conn.commit()


# add the data to the table
for distribuidorPelicula in distribuidoresPeliculas:
    # get the idDistribuidor
    idDistribuidor = distribuidorPelicula[0]
    # get the idPelicula
    tituloPelicula = distribuidorPelicula[1]
    # get the idPelicula
    c.execute('SELECT idPelicula FROM Peliculas WHERE titulo = ?', (tituloPelicula,))
    idPelicula = c.fetchone()[0]    
    # add the distribuidor
    c.execute('INSERT INTO DistribuidoresPeliculasIndiceInvertido VALUES (?, ?)', (idPelicula, idDistribuidor))
    conn.commit()

# close the connection
conn.close()

def getDistribuidoresPeliculas(idPelicula):
    # connect to the database
    conn = sqlite3.connect('Peliculas.db')
    c = conn.cursor()

    # get the distribuidores
    c.execute('SELECT distribuidores FROM DistribuidoresPeliculasIndiceInvertido WHERE idPelicula = ?', (idPelicula,))
    distribuidores = c.fetchall()

    # close the connection
    conn.close()

