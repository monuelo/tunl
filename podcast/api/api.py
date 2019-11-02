from flask import Flask, request
from flask_restful import Resource, Api

import config
from podcast.controller import controller
from podcast.utils import random_string

class CastCRUD(Resource):

    def post(self):
        json = request.get_json()
        image = json.get('image')
        job_id = random_string(string_length=5)

        if image is not None:
            return controller.create_job(job_id, image=image)
        else:
            return controller.create_job(job_id)


app = Flask(__name__)
api = Api(app)

api.add_resource(CastCRUD, "/create/")

def start():
    app.run(host=config.host, port=config.port,
            debug=config.debug)


if __name__ == "__main__":
    start()
