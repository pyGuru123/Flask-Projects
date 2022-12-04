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
		CREATE TABLE quiz (
			index INTEGER PRIMARY KEY AUTOINCREMENT,
			id INTEGER NOT NULL,
			question TEXT NOT NULL,
			category TEXT NOT NULL,
			answer INT NOT NULL
		);
	"""
	cursor.execute(query);
	conn.close()

def populateTable():
	conn = sql.connect(db_path)
	cursor = conn.cursor()
	df = pandas.read_csv('questions.csv')
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