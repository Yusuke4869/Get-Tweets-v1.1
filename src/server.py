from flask import Flask
from threading import Thread

from src.settings import settings

app = Flask(__name__)

@app.route("/")
def main():
    return "Hello World", 200

@app.route("/interval/<int:t>", methods=["GET"])
def set_interval(t):
    try:
        t = int(t)
    except ValueError:
        t = 5

    settings.set_interval(t)
    return f"Set interval to {t}", 200

def running():
    app.run("0.0.0.0")

def doing():
    t = Thread(target=running)
    t.start()