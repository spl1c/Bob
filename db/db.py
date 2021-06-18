import sqlite3
import csv

connection = sqlite3.connect("./db/database.db")  # connect to your DB
cursor = connection.cursor()  # get a cursor

with open('./attachments/jokes.csv','r',newline='',encoding='utf-8') as csvfile:
    reader=csv.reader(csvfile,delimiter='|', skipinitialspace=True, quoting=csv.QUOTE_MINIMAL)
    for row in reader:
        cursor.execute(('INSERT INTO jokes(jokes) VALUES (?)'),(str(row[1]),))
        connection.commit()



cursor.execute("SELECT jokes OVER() AS number FROM jokes")  # execute a simple SQL select query
jobs = cursor.fetchall()  # get all the results from the above query
cursor.close()
connection.close()

print(jobs)