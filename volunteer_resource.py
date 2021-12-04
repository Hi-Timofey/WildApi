from flask import request
from flask_restful import Resource, abort

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from db import db_session
from db.volunteer import Volunteer, VolunteerSchema

VOLUNTEERS_ENDPOINT = '/api/volunteers'

volunteer_schema = VolunteerSchema()

class VolunteersResource(Resource):
    def get(self, id=None):
        if not id:
            return self._get_all_volunteers(), 200
        try:
            return self._get_volunteer_by_id(id), 200
        except BaseException:
            abort(404, message='Volunteer not found')

    def _get_all_volunteers(self):
        db = db_session.create_session()
        volunteers = db.query(Volunteer).all()
        volunteers_json = [volunteer_schema.dump(volunteer) for volunteer in volunteers]
        return volunteers_json

    def _get_volunteer_by_id(self,volunteer_id):
        db = db_session.create_session()
        volunteer = db.query(Volunteer).filter(Volunteer.id==volunteer_id).first()
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


