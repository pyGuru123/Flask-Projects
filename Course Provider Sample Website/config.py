import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")

    MONGODB_SETTINGS = {'db' : 'Course_Enrollment'}
    