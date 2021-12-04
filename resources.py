from flask import request
from flask_restful import Resource, abort, reqparse
import werkzeug

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from db import db_session
from db.photo import Photo
from photo_schema import PhotoSchema
from db.status import Status
from status_schema import StatusSchema
from db.volunteer import Volunteer
from volunteer_schema import  VolunteerSchema

import os
from uuid import uuid4


UPLOAD_DIR = './photos'
PHOTOS_ENDPOINT = '/api/photos'


VOLUNTEERS_ENDPOINT = '/api/volunteers'
STATUSES_ENDPOINT = '/api/statuses'


photo_schema = PhotoSchema()
status_schema = StatusSchema()
volunteer_schema = VolunteerSchema()

class UploadPhoto(Resource):
    def _get_photo_by_id(self, id):
        db = db_session.create_session()
        photo = db.query(Photo).filter(Photo.id == id).first()
        if Photo is None:
            raise ValueError('no such status')
        return photo_schema.dump(photo)

    def get(self, id):
        try:
            return self._get_photo_by_id(id), 200
        except BaseException:
            abort(404, message='Photo not found')

    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('photo', type=werkzeug.datastructures.FileStorage, location='files')
        args = parse.parse_args()
        breakpoint()
        try:
            photo_file = args['photo']
            photo_uuid = uuid4()
            photo_filename = f"photo{photo_uuid}.{photo_file.content_type.split('/')[1]}"

            photo_file.save(os.path.join(UPLOAD_DIR, photo_filename))
            photo = Photo(filename=photo_filename)
            db = db_session.create_session()
            db.add(photo)
        except:
            abort(500, message='Unexpected Error!')
            db.rollback()
        else:
            db.commit()
            return photo_schema.dump(photo), 200


class StatusResource(Resource):
    def _get_all_statuses(self):
        db = db_session.create_session()
        statuses = db.query(Status).all()
        statuses_json = [status_schema.dump(status) for status in statuses]
        return statuses_json

    def _get_status_by_id(self, id):
        db = db_session.create_session()
        status = db.query(Status).filter(Status.id == id).first()
        if status is None:
            raise ValueError('no such status')
        return status_schema.dump(status)

    def get(self, id=None):
        if not id:
            return self._get_all_statuses(), 200

        try:
            return self._get_status_by_id(id), 200
        except BaseException:
            abort(404, message='Status not found')

    def post(self):
        json = request.get_json()
        try:
            db = db_session.create_session()
            status = status_schema.load(json, session=db)
            db.add(status)
            db.commit()
        except IntegrityError as ie:
            print(ie)
            abort(500, message='Unexpected Error!')
        except BaseException as be:
            print(be)
            abort(400, message='Bad Request')
        else:
            return {"status_id":status.id}, 201



class VolunteersResource(Resource):
    def get(self, id=None):
        breakpoint()
        if not id:
            status_id = request.args.get('status_id')
            return self._get_all_volunteers(status_id), 200

        try:
            return self._get_volunteer_by_id(id), 200
        except BaseException:
            abort(404, message='Volunteer not found')

    def _get_all_volunteers(self, status_id):
        db = db_session.create_session()
        if status_id:
            volunteers =  db.query(Volunteer).filter(Volunteer.volunteer_status_id == status_id).all()
        else:
            volunteers = db.query(Volunteer).all()
        volunteers_json = [volunteer_schema.dump(volunteer) for volunteer in volunteers]
        return volunteers_json

    def _get_volunteer_by_id(self,volunteer_id):
        db = db_session.create_session()
        volunteer = db.query(Volunteer).filter(Volunteer.id==volunteer_id).first()
        if volunteer is None:
            raise ValueError('no such volunteer')
        volunteer_json = volunteer_schema.dump(volunteer)
        return volunteer_json

    def post(self):
        json = request.get_json()
        try:
            db = db_session.create_session()
            breakpoint()
            volunteer = volunteer_schema.load(json, session=db)
            db.add(volunteer)
            db.commit()
        except IntegrityError as ie:
            print(ie)
            abort(500, message='Unexpected Error!')
        except BaseException as be:
            print(be)
            abort(400, message='Bad Request')
        else:
            return {"volunteer_id":volunteer.id}, 201

    def patch(self, id=None):
        json = request.get_json()
        if not id:
            abort(400, message='Bad Request')
        try:
            db = db_session.create_session()
            volunteer = db.query(Volunteer).filter(Volunteer.id==id).first()
            if volunteer is None:
                raise  ValueError

            for key in json:
                setattr(volunteer, key, json[key])

            db.add(volunteer)
            db.commit()
            # print(json)
            # print(volunteer)
            # breakpoint()

        except ValueError as ve:
            abort(400, message='Bad Request')
        except BaseException as be:
            breakpoint()
            abort(500, message='Unexpected Error!')
        else:
            return {"volunteer_id":volunteer.id}, 201



