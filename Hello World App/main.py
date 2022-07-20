from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def helloworld():
	return render_template("index.html", data="world")

@app.route("/<string:name>")
def helloname(name):
	return render_template("index.html", data=name)

if __name__ == "__main__":
	app.run(debug=False)