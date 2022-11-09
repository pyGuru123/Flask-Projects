from flask_wtf import FlaskForm
from wtforms import  StringField, IntegerField, TextAreaField, BooleanField, RadioField
from wtforms.validators import  InputRequired, Length

class EmpForm(FlaskForm):
	name = StringField("Name", validators=[InputRequired(), Length(max=15)])
	work = TextAreaField("Work", validators=[InputRequired(), Length(max=50)])
	salary = IntegerField("Salary", validators=[InputRequired()])
	language = RadioField("Language", choices=["Python", "C", "Java"], validators=[InputRequired()])
	available = BooleanField("Available", default="checked")