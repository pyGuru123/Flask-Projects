import requests
from flask import Flask, render_template, url_for, request, session, redirect
from flask_session import Session
from model import fetchQuestions

app = Flask(__name__, static_url_path='/static')
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


@app.route('/', methods=["GET", "POST"])
@app.route('/login', methods=["GET", "POST"])
def loginPage():
	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]
		print(username)
		if username:
			session['username'] = username
			return redirect(url_for('categoriesPage'))

	return render_template('login.html')

@app.route('/signup', methods=["GET", "POST"])
def signupPage():
	return render_template('signup.html')

@app.route('/categories', methods=["GET", "POST"])
def categoriesPage():
	if session.get('category'):
		session.pop('category')

	if request.method == "POST":
		category = request.form['category']
		if not session.get('category'):
			session['category'] = category
			session.modified = True
		return redirect(url_for('instructionsPage'))

	return render_template('categories.html', username=session['username'])

@app.route('/instructions', methods=["GET", "POST"])
def instructionsPage():
	category = session["category"]
	img = categories[category]
	data = [category, img]
	return render_template('instructions.html', data=data)

@app.route('/quiz', methods=["GET", "POST"])
def quizPage():
	if request.method == "POST":
		if not session.get('questions'):
			questions = fetchQuestions(session['category'])
			session['questions'] = questions

		questions = session['questions']
		id = int(request.form['nextId'])
		if id <= 10:
			question = questions[id-1]
			icon = categories[question[3]]

			data = {
				'id' : id,
				'question' : question[1],
				'description' : question[2],
				'category' : question[3],
				'icon' : icon,
				'price' : question[4],
				'pic' : icon.rstrip('.png') + str(id)
			}

			return render_template('quiz.html', data=data)
		else:
			return redirect(url_for('submitPage'))

@app.route('/submit', methods=["GET", "POST"])
def submitPage():
	return render_template('submit.html')

if __name__ == "__main__":
	app.run(debug=True)