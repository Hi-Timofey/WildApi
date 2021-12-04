# -*- coding: utf-8 -*-
from flask import Flask
from flask_restful import Api

# from db.volunteer import Volunteer
from volunteer_resource import VolunteersResource, VOLUNTEERS_ENDPOINT
from db import db_session

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return 'working'

def create_app():
    db_session.global_init_sqlite('db.sqlite')
    api = Api(app)
    api.add_resource(VolunteersResource, VOLUNTEERS_ENDPOINT, f'{VOLUNTEERS_ENDPOINT}/<id>')

    app.config.from_envvar('API_CONFIG')
    app.run(host='0.0.0.0', port=8080)


if __name__ == '__main__':
    create_app()
