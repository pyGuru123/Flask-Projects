from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html", data=None)
	
@app.route("/word", methods=["GET", "POST"])
def getMeaning():
	if request.method == "POST":
		word = request.form["word"]
		print(word)
		if word:
			data = searchWord(word)
			data.insert(0, word)
		
			return render_template("index.html", data=data)
		
		
def searchWord(word):
	url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
	r = requests.get(url)
	data = r.json()
	if not 'message' in data:
		phonetic = data[0]["phonetics"][0]["text"]
		pos = data[0]["meanings"][0]["partOfSpeech"]
		definitions = data[0]['meanings'][0]['definitions']
	
		return [phonetic, pos, definitions]
		
	return [data['message']]

if __name__ == "__main__":
	app.run(debug=True)