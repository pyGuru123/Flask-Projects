import pandas
import csv
import os
import sqlite3 as sql

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "database.db")

if not os.path.exists(db_path):
	conn = sql.connect(db_path)
	cursor = conn.cursor()

	query = """
		CREATE TABLE credentials (
			username TEXT PRIMARY KEY NOT NULL,
			email TEXT UNIQUE NOT NULL,
			password TEXT NOT NULL
		);
	"""
	cursor.execute(query);

	query = """
		CREATE TABLE quiz (
			index INTEGER PRIMARY KEY AUTOINCREMENT,
			id INTEGER NOT NULL,
			question TEXT NOT NULL,
			description TEXT,
			category TEXT NOT NULL,
			answer INT NOT NULL
		);
	"""
	cursor.execute(query);
	conn.close()

def registerUser(username, email, password):
	conn = sql.connect(db_path)
	cursor = conn.cursor()
	query = """
		INSERT INTO credentials VALUES (?, ?, ?);
	"""
	cursor.execute(query, (username, email, password))
	conn.commit()
	conn.close()

def fetchUsernames():
	conn = sql.connect(db_path)
	cursor = conn.cursor()
	query = """
		SELECT username from credentials;
	"""
	cursor.execute(query)
	usernames = cursor.fetchall()
	conn.close()

	allusers = [username[0] for username in usernames]
	return allusers

def populateTable():
	conn = sql.connect(db_path)
	cursor = conn.cursor()
	df = pandas.read_excel('questions.xlsx')
	df.to_sql('questions', conn, if_exists="fail", index=False)
	conn.close()

def fetchQuestions(category):
	conn = sql.connect(db_path)
	cursor = conn.cursor()
	query = """
		SELECT * from questions where category = ?;
	"""
	cursor.execute(query, (category, ))
	questions = cursor.fetchall()
	conn.close()

	return questions