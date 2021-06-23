import sqlite3
import csv

connection = sqlite3.connect("./db/database.db")  # connect to your DB
cursor = connection.cursor()  # get a cursor




cursor.execute("SELECT jokes, ROW_NUMBER() OVER() AS number FROM jokes WHERE status=?",('pending',))
jobs = cursor.fetchall() 
cursor.close()
connection.close()

for i in jobs:
    print(i)