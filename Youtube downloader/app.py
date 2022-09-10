from flask import Flask, render_template, request
from pytube import YouTube

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")
	
@app.route("/download", methods=["POST", "GET"])
def downloadVideo():
	if request.method == "POST":
		url = request.form["videourl"]
		yt = YouTube(url)
		title = yt.title
		thumbnail = yt.thumbnail_url
		streams = yt.streams
		print(thumbnail)
		data = [title, thumbnail, streams]
		
		return render_template("downloadPage.html", data=data)
	
# https://youtu.be/jiY4PgUW7aA
if __name__ == "__main__":
	app.run(debug=True)