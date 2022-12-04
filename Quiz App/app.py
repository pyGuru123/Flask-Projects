import requests
from flask import Flask, render_template, url_for, request

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
@app.route('/login', methods=["GET", "POST"])
def login():
	return render_template('login.html')

@app.route('/signup', methods=["GET", "POST"])
def signup():
	return render_template('signup.html')

@app.route('/categories', methods=["GET", "POST"])
def categories():
	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]

		return render_template('categories.html', username=username)

if __name__ == "__main__":
	app.run(debug=True)