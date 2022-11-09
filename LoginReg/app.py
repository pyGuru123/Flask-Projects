from flask import Flask, render_template, redirect, url_for
from forms import EmpForm
import webbrowser

app = Flask(__name__)
app.config["SECRET_KEY"] = "qwertyuiop"

employees = [
	{
		"name" : "John Doe",
		"work": "Developer",
		"salary" : 52000,
		"language" : "Python",
		"available" : True
	}
]

@app.route("/", methods=["GET", "POST"])
def index():
	form = EmpForm()
	return render_template("index.html", form=form)
	
if __name__ == "__main__":
	app.run(debug=True)
	webbrowser.open_new_tab("http://127.0.0.1:5000/")