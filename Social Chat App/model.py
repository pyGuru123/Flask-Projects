import sqlite3 as sql
from os import path
from datetime import datetime

BASE_DIR = path.dirname(path.abspath(__file__))
db_path = path.join(BASE_DIR, "database.db")

if not path.exists(db_path):
	con = sql.connect(db_path)
	cursor = con.cursor()
	query = """
			CREATE TABLE posts (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				name TEXT NOT NULL,
				post TEXT NOT NULL,
				datetime TIMESTAMP
			);
		"""
	cursor.execute(query)
	con.close()
	
def create_post(name, content, time):
	con = sql.connect(db_path)
	cursor = con.cursor()
	query = """
		INSERT INTO posts (name, post, datetime) values (?, ?, ?);
	"""
	cursor.execute(query, (name, content, time))
	con.commit()
	con.close()
	
def fetch_posts():
	con = sql.connect(db_path)
	cursor = con.cursor()
	query = """
		SELECT * FROM posts;
	"""
	cursor.execute(query)
	posts = cursor.fetchall()
	con.close()
	return posts