import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or b'2\xcc!\xcc\xd3\xc2\xab,\xcb\xff\x7f\x906\xd5\x7f\x1c'
    GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

    print(GITHUB_TOKEN, SECRET_KEY)