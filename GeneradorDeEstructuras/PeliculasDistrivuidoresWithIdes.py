#adds ids to the table of PeliculasDistibuidores
# Path: GeneradorDeEstructuras\PeliculasDistrivuidoresWithIdes.py
# gets the id of the movie from the tables peliculas and insert it in the table PeliculasDistibuidores where the tile is the same
import sqlite3

# connect to database
conn = sqlite3.connect('./dataBase/Peliculas.db')
c = conn.cursor()

c.execute( "SELECT title, distributors FROM PeliculasDistibuidores")
rows = c.fetchall()

#adds a column named id 
c.execute("ALTER TABLE PeliculasDistibuidores ADD COLUMN id INTEGER")

for row in rows:
    c.execute("SELECT id FROM peliculas WHERE title = ?", (row[0],))
    id = c.fetchone()
    c.execute("UPDATE PeliculasDistibuidores SET id = ? WHERE title = ?", (id[0], row[0]))
    conn.commit()

# close the connection
conn.close()
