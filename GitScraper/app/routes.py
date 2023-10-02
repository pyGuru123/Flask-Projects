from app import app
from app.scraper import User, Repository
from app.scripts import fetch_repo_stats

import json
from flask import render_template, url_for, request, Response, session, flash, redirect

data = {'reponame': 'GitScraper', 'author': 'pyGuru123', 'about': 'A Flask website to scrape github profiles.', 'weblink': 'github.com/pyGuru123/GitScraper', 'topics': ['github', 'scraper', 'webscraping', 'githubscrapapi', 'githubprofile'], 'issues': '0', 'pullrequests': '0', 'forks': '0', 'stars': '0', 'watching': '0', 'commits': '9', 'repotype': 'Public', 'languages': {'Python': '50.6', 'HTML': '40.5', 'CSS': '4.7', 'JavaScript': '4.1', 'Shell': '0.1'}}

@app.route("/")
@app.route("/home")
@app.route("/index", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form.get('username')
        if username:
            try:
                user = User(username.strip('@'))
                data = user.get_full_info()
                return render_template("index.html", index=True, data=data)
            except:
                flash("Username doesn't exist")
                return redirect("/home")
    return render_template("index.html", index=True, data=data)

@app.route("/allrepostats/<username>")
def all_repo_stats(username):
    result = fetch_repo_stats(username)
    if result:
        json_data = json.dumps(result)
        return json_data
    else:
        return json.dumps([])

@app.route('/exportprofile', methods=["POST"])
def export_profile():
    username = request.form.get("username")
    data = request.form.get("data")
    filename = f"{username}.json"
    # content = json.loads(data)
    return Response(data,
        mimetype='application/json',
        headers={'Content-Disposition':f'attachment;filename={filename}'}
    )

@app.route("/repo")
@app.route("/repository", methods=["GET", "POST"])
def repository():
    if request.method == "POST":
        repo_url = request.form.get("repo")
        if repo_url:
            try:
                repo = Repository(repo_url)
                data = repo.get_full_info()
                print(data)
                return render_template("repository.html", repo=True, data=data)
            except:
                flash("Repository doesn't exist")
                return redirect("/repo")

    return render_template("repository.html", repo=True, data=None)

@app.route("/langs")
@app.route("/languages")
def languages():
    return render_template("languages.html", lang=True)

@app.route("/about")
def about():
    return render_template("about.html", about=True)
