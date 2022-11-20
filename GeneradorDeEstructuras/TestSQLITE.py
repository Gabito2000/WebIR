#creates a sqlite database to test the code
#


import sqlite3
import sys

# create database
conn = sqlite3.connect('./dataBase/Peliculas.db')
c = conn.cursor()

# create table
c.execute('''DROP TABLE IF EXISTS Peliculas''')
c.execute('''CREATE TABLE Peliculas
                (id integer primary key, nombre text, genero text, director text, anio integer, duracion integer)''')


# insert data
c.execute("INSERT INTO Peliculas VALUES (1, 'El Padrino', 'Drama', 'Francis Ford Coppola', 1972, 175)")
c.execute("INSERT INTO Peliculas VALUES (2, 'El Padrino 2', 'Drama', 'Francis Ford Coppola', 1974, 202)")

# save data to database
conn.commit()

# reed data
c.execute("SELECT * FROM Peliculas")
print(c.fetchall())

# close connection
conn.close()


