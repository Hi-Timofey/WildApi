# -*- coding: utf-8 -*-
from flask import Flask
from flask_restful import Api

# from db.volunteer import Volunteer
from db import db_session

from db.status import Status
from db.volunteer import Volunteer

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return 'working'

def create_app():
    db_session.global_init_sqlite('db.sqlite')

    from resources import VolunteersResource, VOLUNTEERS_ENDPOINT
    from resources import StatusResource, STATUSES_ENDPOINT


    api = Api(app)
    api.add_resource(VolunteersResource, VOLUNTEERS_ENDPOINT, f'{VOLUNTEERS_ENDPOINT}/<id>')
    api.add_resource(StatusResource, STATUSES_ENDPOINT, f'{STATUSES_ENDPOINT}/<id>')

    app.config.from_envvar('API_CONFIG')
    app.run(host='0.0.0.0', port=8080)


if __name__ == '__main__':
    create_app()
