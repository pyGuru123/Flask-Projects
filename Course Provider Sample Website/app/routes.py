from app import app, db
from app.models import User, Course, Enrollment
from flask import render_template, request, json, Response

courseData = [{"courseID":"1111","title":"PHP 101","description":"Intro to PHP","credits":3,"term":"Fall, Spring"}, {"courseID":"2222","title":"Java 1","description":"Intro to Java Programming","credits":4,"term":"Spring"}, {"courseID":"3333","title":"Adv PHP 201","description":"Advanced PHP Programming","credits":3,"term":"Fall"}, {"courseID":"4444","title":"Angular 1","description":"Intro to Angular","credits":3,"term":"Fall, Spring"}, {"courseID":"5555","title":"Java 2","description":"Advanced Java Programming","credits":4,"term":"Fall"}]

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
    return render_template("register.html", register=True)

@app.route('/login')
def login():
    return render_template("login.html", login=True)

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