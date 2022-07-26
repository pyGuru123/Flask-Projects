from flask import Flask, render_template, request
import requests

app = Flask(__name__)

api_key = '37f96394ffe8b6cca1110af3d8270604c711c688'

@app.route("/")
def index():
	return render_template("index.html", result=None)
	
@app.route("/aqi", methods=["GET", "POST"])
def getAQI():
	if request.method == "POST":
		city = request.form["city"]
		url = 'http://api.waqi.info/feed/' + city + '/?token=' + api_key
		
		r = requests.get(url)
		data = r.json()['data']
		
		result = {}
		result['city'] = city
		result['aqi'] = data['aqi']
		result['stats'] = data['iaqi']
		if 'p' in result['stats']:
			del result['stats']['p']
		return render_template("index.html", result=result)



if __name__ == "__main__":
	app.run(debug=True)