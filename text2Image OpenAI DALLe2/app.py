from flask import Flask, render_template, request
import requests

app = Flask(__name__)

key = "Bearer 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"
endpoint = "https://api.openai.com/v1/images/generations"
headers = {"Content-Type": "application/json", "Authorization": key}

@app.route("/", methods=["POST", "GET"])
def home():
	if request.method == "POST":
		text = request.form["desc"]
		data = {
    "prompt": text,
    "n": 3,
    "size": "1024x1024"
    }
		r = requests.post(endpoint, json=data,headers=headers)
		print(r.json())
		
		imgs = r.json()["data"]
		images = [img['url'] for img in imgs]
		#print(images)
		return render_template("index.html", images=images, text=text)
	return render_template("index.html", images=None, text=None)
	
if __name__ == "__main__":
	app.run(debug=True)