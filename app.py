# -*- coding: utf-8 -*-
from flask import Flask, send_from_directory
from flask_restful import Api

# from db.volunteer import Volunteer
from db import db_session

from db.status import Status
from db.volunteer import Volunteer

app = Flask(__name__)


@app.route('/photos/<path:filename>', methods=['GET'])
def download_photo(filename):
    return send_from_directory("photos/", filename, as_attachment=True)

def create_app():
    db_session.global_init_sqlite('db.sqlite')

    from resources import VolunteersResource, VOLUNTEERS_ENDPOINT
    from resources import StatusResource, STATUSES_ENDPOINT
    from resources import UploadPhoto, PHOTOS_ENDPOINT


    api = Api(app)
    api.add_resource(VolunteersResource, VOLUNTEERS_ENDPOINT, f'{VOLUNTEERS_ENDPOINT}/<id>')
    api.add_resource(StatusResource, STATUSES_ENDPOINT, f'{STATUSES_ENDPOINT}/<id>')
    api.add_resource(UploadPhoto,PHOTOS_ENDPOINT,PHOTOS_ENDPOINT, f'{PHOTOS_ENDPOINT}/<id>')

    app.config.from_envvar('API_CONFIG')
    app.run(host='0.0.0.0', port=8080)


if __name__ == '__main__':
    create_app()
