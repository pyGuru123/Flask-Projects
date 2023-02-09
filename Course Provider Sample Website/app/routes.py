from app import app, db
from app.models import User, Course, Enrollment
from app.forms import LoginForm, RegisterForm
from flask import render_template, request, json, Response, flash, redirect, url_for, session

@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html", login=False, index=True)

@app.route('/courses')
@app.route('/courses/<term>')
def courses(term="2019"):
    courseData = Course.objects.order_by("+courseID")
    return render_template("courses.html", courseData=courseData, courses=True, term=term)

@app.route('/register', methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect("/index")

    form = RegisterForm()
    if form.validate_on_submit():
        user_id = User.objects.count() + 1

        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User(user_id=user_id, first_name=first_name, last_name=last_name, email=email)
        user.set_password(password)
        user.save()

        flash("You are successfully registered !", "success")
        return redirect("/login")
    return render_template("register.html", form=form, register=True,  title="New User Registration")

@app.route('/login', methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect("/index")

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.objects(email=email).first()
        if user and user.get_password(password):
            flash(f"Hello {user.first_name}, You are now loggedin", "success")
            session["user_id"] = user.user_id
            session["username"] = user.first_name
            return redirect("/index")
        else:
            flash("Incorrect email or password", "danger")
    return render_template("login.html", login=True, form=form, title="Login")

@app.route("/logout")
def logout():
    session.pop("user_id")
    session.pop("username", None)
    flash("You logged out succesfully", "success")
    return redirect(url_for("index"))


@app.route('/enrollment', methods=["GET", "POST"])
def enrollment():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    courseID = request.form.get("courseID")
    courseTitle = request.form.get("title")
    user_id = session.get("user_id")

    if courseID:
        if Enrollment.objects(user_id=user_id, courseID=courseID):
            flash(f"Already enrolled in {courseTitle} course", "danger")
            return redirect(url_for('courses'))
        else:
            Enrollment(user_id=user_id, courseID=courseID).save()
            flash(f"You are enrolled in {courseTitle} successfully", "success")

    classes = list(User.objects.aggregate(*[
        {
            '$lookup': {
                'from': 'enrollment', 
                'localField': 'user_id', 
                'foreignField': 'user_id', 
                'as': 'r1'
            }
        }, {
            '$unwind': {
                'path': '$r1', 
                'includeArrayIndex': 'r1_id', 
                'preserveNullAndEmptyArrays': False
            }
        }, {
            '$lookup': {
                'from': 'course', 
                'localField': 'r1.courseID', 
                'foreignField': 'courseID', 
                'as': 'r2'
            }
        }, {
            '$unwind': {
                'path': '$r2', 
                'preserveNullAndEmptyArrays': False
            }
        }, {
            '$match': {
                'user_id': user_id
            }
        }, {
            '$sort': {
                'courseID': 1
            }
        }
    ]))

    return render_template("enrollment.html", enrollment=True, classes=classes)

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
    users = User.objects.all()
    return render_template("user.html", users=users)