#Loads a csv file to a database with the first column as the primary key and the rest of the columns as the rest of the columns
# the csv file must have the following format (without the #):
# # NameColumn1, ..., NameColumnN
# # idValue, ..., valueN

import sqlite3
import sys
import shutil
import os

#gets the name of the csv file
csvFileName = sys.argv[1]

if csvFileName is None:
    #do for all csv files in the directory
    for file in os.listdir('.'):
        if file.endswith('.csv'):
            #if contains a number replace remove it
            if any(char.isdigit() for char in file):
                file = ''.join([i for i in file if not i.isdigit()])
            loadCsv(file.replace('.csv', ''))
else:
    loadCsv(csvFileName)

    

def loadCsv(csvFileName):
    # connect to the database
    conn = sqlite3.connect('Peliculas.db')
    c = conn.cursor()
    
    # get the name of the columns
    columns = []
    with open(csvFileName + '.csv', 'r') as f:
        columns = f.readline().split(',')
        columns = [column.replace('\n', '') for column in columns]

    # creates the table
    c.execute('DROP TABLE IF EXISTS ' + csvFileName)
    c.execute('CREATE TABLE ' + csvFileName + ' (' + columns[0] + ' INTEGER PRIMARY KEY, ' + ', '.join(columns[1:]) + ')')
    conn.commit()

    # adds the data to the table
    with open(sys.argv[1] + '.csv', 'r') as f:
        f.readline()
        for line in f:
            values = line.split(',')
            values = [value.replace('\n', '') for value in values]
            c.execute('INSERT INTO ' + csvFileName + ' VALUES (' + ', '.join(['?'] * len(values)) + ')', values)
            conn.commit()

    # close the connection
    conn.close()

    # move the csv file to the csv directory
    shutil.move(csvFileName + '.csv', 'csv/' + csvFileName + '.csv')

    
