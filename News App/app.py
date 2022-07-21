import requests
from flask import Flask, render_template

app = Flask(__name__)


api_key = "0d48912cbe864506a076a3b74df00c79"
endpoint = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}"

@app.route("/")
def index():
	r = requests.get(endpoint)
	response = r.json()
	articles = response["articles"]
	return render_template("index.html", articles=articles)

@app.route("/<string:country>")
def fetchCountryHeadlines(country):
	endpoint = f"https://newsapi.org/v2/top-headlines?country={country}&apiKey={api_key}"

	r = requests.get(endpoint)
	response = r.json()
	articles = response["articles"]
	return render_template("index.html", articles=articles)

if __name__ == "__main__":
	app.run(debug=True)