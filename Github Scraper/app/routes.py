from app import app
from flask import render_template, url_for

@app.route("/")
@app.route("/home")
@app.route("/index")
def index():
    return render_template("index.html", index=True)

@app.route("/repo")
@app.route("/repository")
def register():
    return render_template("repository.html", repo=True)

@app.route("/langs")
@app.route("/languages")
def languages():
    return render_template("languages.html", lang=True)

@app.route("/about")
def about():
    return render_template("about.html", about=True)
