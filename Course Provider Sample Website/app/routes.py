from app import app, db
from app.models import User, Course, Enrollment
from app.forms import LoginForm, RegisterForm
from flask import render_template, request, json, Response, flash, redirect

@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html", login=False, index=True)

@app.route('/courses')
@app.route('/courses/<term>')
def courses(term="2019"):
    courseData = Course.objects.all()
    return render_template("courses.html", courseData=courseData, courses=True, term=term)

@app.route('/register')
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_id = User.objects.count() + 1
        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
    return render_template("register.html", form=form, title="New User Registration")

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.objects(email=email).first()
        if user and user.get_password(password):
            flash(f"Hello {user.first_name}, You are now loggedin", "success")
            return redirect("/index")
        else:
            flash("Incorrect email or password", "danger")
            form = LoginForm()
            return render_template("login.html", form=form, title="Login")
    return render_template("login.html", form=form, title="Login")

@app.route('/enrollment', methods=["GET", "POST"])
def enrollment():
    if request.method == "POST":
        courseID = request.form.get("courseID")
        title = request.form.get("title")
        term = request.form.get("term")
        data = {
            "courseID" : courseID,
            "title" : title,
            "term" : term
        }
    return render_template("enrollment.html", enrollment=True, data=data)

@app.route('/api')
@app.route('/api/<id>')
def api(id=None):
    courseData = Course.objects.all()
    if not id:
        jData = courseData
    else:
        jData = courseData[int(id)]

    return Response(json.dumps(jData), mimetype="application/json")

@app.route('/user')
def user():
    # User(user_id=1, first_name='Bruce', last_name='Wayne', email='bw123@gmail.com', password='password').save()
    # User(user_id=2, first_name='Mary', last_name='Jane', email='mj@gmail.com', password='password123').save()

    users = User.objects.all()
    return render_template("user.html", users=users)