import requests
from flask import Flask, render_template, url_for, request, session
from flask_session import Session
from model import fetchQuestions

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

categories = {
	'Baby' : 'baby.png',
	'Books' : 'books.png',
	'DVD & Bluray' : 'camera.png',
	'Car & Bike' : 'car.png',
	'Computers' : 'computer.png',
	'Beauty' : 'cosmetics.png',
	'Grocery' : 'food.png',
	'Musical Instruments' : 'guitar.png',
	'Toys' : 'horse.png',
	'Kitchen & Home' : 'house.png',
	'Lighting' : 'light.png',
	'Sports' : 'sports.png',
	'Stationary' : 'stationary.png',
	'Vinyl' : 'vinyl.png',
	'Smartphone' : 'phone.png'
}

questions = []

@app.route('/', methods=["GET", "POST"])
@app.route('/login', methods=["GET", "POST"])
def loginPage():
	return render_template('login.html')

@app.route('/signup', methods=["GET", "POST"])
def signupPage():
	return render_template('signup.html')

@app.route('/categories', methods=["GET", "POST"])
def categoriesPage():
	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]

		return render_template('categories.html', username=username, 
													categories=categories)

@app.route('/instructions', methods=["GET", "POST"])
def instructionsPage():
	if request.method == "POST":
		category = request.form["category"]
		img = categories[category]
		data = [category, img]
		if not session.get('category'):
			session['category'] = category
		return render_template('instructions.html', data=data)

@app.route('/quiz/<int:id>', methods=["GET", "POST"])
def quizPage(id):
	if request.method == "POST":
		if not session.get('questions'):
			questions = fetchQuestions(session['category'])
			session['questions'] = questions
			session['id'] = id

		questions = session['questions']
		question = questions[id-1]
		session['id'] += 1
		return render_template('quiz.html', data=questions[id])

if __name__ == "__main__":
	app.run(debug=True)