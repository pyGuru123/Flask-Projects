from datetime import datetime
from flask import Flask, render_template, request
from model import create_post, fetch_posts

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def homepage():
	if request.method == "POST":
		username = request.form.get("username", None)
		content = request.form.get("content", None)
		dt = datetime.now()
		if username and content:
			create_post(username, content, dt)

	posts = fetch_posts()
	return render_template("index.html", posts=posts)

if __name__ == "__main__":
	app.run()