# inport csv to database sqlite3
# the csv file is in ../data/titles.csv
# the database is in dataBase/Peliculas.db
# the table is in PeliculasDistibuidores
# the table has 3 columns: title, distributors
# the csv has 4 columns: Id;title;Distributor;type

import csv
import sqlite3

# connect to database
conn = sqlite3.connect('./dataBase/Peliculas.db')
c = conn.cursor()

# create table

c.execute('''DROP TABLE IF EXISTS PeliculasDistibuidores''')
c.execute('''CREATE TABLE PeliculasDistibuidores
                (title text, distributors text)''')

# open csv file
with open('../data/titles.csv', 'r', encoding="utf8") as f:
    # reeds the csv with the delimiter ;
    reader = csv.reader(f, delimiter=';')
    # skip the first line
    next(reader)
    # insert the data in the table
    for row in reader:
        # gets the existing distruvibutors
        c.execute(
            "SELECT distributors FROM PeliculasDistibuidores WHERE title = ?", (row[1],))
        distributors = c.fetchone()
        # if the movie is not in the table
        if distributors is None:
            # insert the movie and the distributor
            c.execute(
                "INSERT INTO PeliculasDistibuidores VALUES (?, ?)", (row[1], row[2]))

        # if the movie is in the table
        else:
            # cheks if the distributor is already in the table
            if distributors[0].find(row[2]) == -1:
                # splits the distributors
                distributorsAux = distributors[0].split(',')
                distributorsAux.append(row[2])
                distributorsAux.sort()
                distributors = ','.join(distributorsAux)
                # insert the movie and the distributor
                c.execute(
                    "UPDATE PeliculasDistibuidores SET distributors = ? WHERE title = ?", (distributors, row[1]))
        conn.commit()

# close the connection
conn.close()
