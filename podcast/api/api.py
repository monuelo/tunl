from flask import Flask, request
import config
import json

app = Flask(__name__)


def start():
    app.run(host=config.host, port=config.port,
            debug=config.debug)


@app.route("/", methods=["GET"])
def index():
    return "Hello, Podcast!"


@app.route("/create", methods=["POST"])
def create_container():
    if request.method == "POST":
        print(json.loads(request.data))
        return "Create, World!"


if __name__ == "__main__":
    start()
