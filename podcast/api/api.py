from flask import Flask, request
from flask_cors import CORS
import json

import config
from podcast.controller import controller
from podcast.utils import random_string

app = Flask(__name__)
cors = CORS(app, resources={r"/create*": {"origins": "*"}})


@app.route("/create", methods=["POST"])
def create_container():
    if request.method == "POST":
        req = request.get_json()
        image = req.get('image')
        job_id = random_string(string_length=5)

        if image is not None:
            return json.dumps(controller.create_job(job_id, image=image))
        else:
            return json.dumps(controller.create_job(job_id))


def start():
    app.run(host=config.host, port=config.port,
            debug=config.debug)


if __name__ == "__main__":
    start()
