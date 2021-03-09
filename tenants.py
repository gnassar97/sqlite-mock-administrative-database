import sqlite3
import sys
import random
from random import randrange
from datetime import datetime, timedelta, date, time

db = sys.argv[1]
conn = sqlite3.connect(db)
cursor = conn.cursor()
cursor.execute('PRAGMA foreign_keys=ON;')   
conn.commit()

def main():

	
	price_range()
	#tenants()

def price_range():
	left_range_input = input("What is the minimum price?: ")
	right_range_input = input("What is the maximum price?: ")
	suit_input = input("What is the suit type?: ")

	cursor.execute("SELECT sID, price FROM Suits WHERE ? LIKE type AND price >= ? AND price <= ? ORDER BY price ASC", (suit_input, left_range_input, right_range_input))
	suites = cursor.fetchall()
	conn.commit()

	for row in suites:
		print(row)

def tenants():
	id_input = input("What is the suit ID?: ")


	
	#cursor.execute(create_query)
	#conn.commit()

	cursor.execute("SELECT * FROM Tenants WHERE sID = ? AND yearOfOccup < 2000;", (id_input,))

	col1 = cursor.description[0][0]
	col2 = cursor.description[1][0]
	col3 = cursor.description[2][0]
	col4 = cursor.description[3][0]

	create_query = '''CREATE TABLE selected_tenants (
  %s    INTEGER,
  %s     TEXT,
  %s INTEGER,
  %s     INTEGER,
  PRIMARY KEY (tID),
  FOREIGN KEY (sID) REFERENCES Suits
);''' % (col1,col2,col3,col4)

	

	data = cursor.fetchall()
	#print(data)
	conn.commit()

	cursor.execute("drop table if exists selected_tenants;")
	conn.commit()
	cursor.execute(create_query)
	conn.commit()

	#cursor.execute("SELECT * FROM selected_tenants")
	#print("name of the first column: " + cursor.description[0][0])
	#conn.commit()

	for row in data:
		i_tID = row[0]
		i_name = row[1]
		i_year = row[2]
		i_sID = row[3]
		tenant_data = (i_tID, i_name, i_year, i_sID)
		print(tenant_data)
		cursor.execute("INSERT INTO selected_tenants(tID, name, yearOfOccup, sID) VALUES (?,?,?,?)", tenant_data)
		conn.commit()












main()
conn.close()