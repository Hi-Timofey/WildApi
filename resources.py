from flask import request
from flask_restful import Resource, abort, reqparse
import werkzeug

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from db import db_session

from db.video import Video
from video_schema import VideoSchema

from db.photo import Photo
from photo_schema import PhotoSchema
from db.status import Status
from status_schema import StatusSchema
from db.volunteer import Volunteer
from volunteer_schema import VolunteerSchema

import os
from uuid import uuid4


PHOTOS_DIR = './photos'
VIDEOS_DIR = './videos'
PHOTOS_ENDPOINT = '/api/photos'
VIDEOS_ENDPOINT = '/api/videos'


VOLUNTEERS_ENDPOINT = '/api/volunteers'
STATUSES_ENDPOINT = '/api/statuses'

video_schema = VideoSchema()
photo_schema = PhotoSchema()
status_schema = StatusSchema()
volunteer_schema = VolunteerSchema()


class UploadVideo(Resource):

    def delete(self, id=None):
        if not id:
            abort(400, message='Bad Request: no id')
        try:
            db = db_session.create_session()
            photo = db.query(Video).filter(Video.id == id).first()
            db.delete(Video)
        except BaseException as be:
            abort(500, message=f'Unexpected Error: {be}')
        else:
            db.commit()
            return {"video_id": id}, 201

    def _get_video_by_id(self, id):
        db = db_session.create_session()
        video = db.query(Video).filter(Video.id == id).first()
        if video is None:
            raise ValueError('no such video')
        return video_schema.dump(video)

    def _get_all_video_by_id(self, owner_id):
        db = db_session.create_session()
        videos = db.query(Video).filter(Video.owner_id == owner_id).all()
        if videos is None or videos == []:
            raise ValueError("not found")
        videos_json = [video_schema.dump(video) for video in videos]
        return videos_json

    def get(self, id=None):
        if not id:
            owner_id = request.args.get("owner_id")
            try:
                return self._get_all_video_by_id(owner_id), 200
            except ValueError as ve:
                abort(404, message=f'ValueError: {ve}')
            except BaseException as be:
                abort(500, message=f'Unexpected error: {be}')

        try:
            return self._get_video_by_id(id), 200
        except ValueError as ve:
            abort(404, message=f'ValueError: {ve}')
        except BaseException as be:
            abort(500, message='Unexpected error: {be}')

    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument(
            'video',
            type=werkzeug.datastructures.FileStorage,
            location='files')
        parse.add_argument('owner_id', type=int)
        args = parse.parse_args()
        try:
            video_file = args['video']
            video_uuid = uuid4()
            video_filename = f"video{video_uuid}.{video_file.content_type.split('/')[1]}"

            breakpoint()
            db = db_session.create_session()

            video = Video(filename=video_filename)

            if args['owner_id']:
                volun = db.query(Volunteer).filter(
                    Volunteer.id == int(args['owner_id'])).first()
                if volun is None:
                    raise ValueError
                video.owner = volun

            video_file.save(os.path.join(VIDEOS_DIR, video_filename))
            db.add(video)
        except ValueError as ve:
            abort(400, message=f'ValueError: {ve}')
            db.rollback()
        except BaseException as be:
            abort(500, message=f'Unexpected Error: {be}')
            db.rollback()
        else:
            db.commit()
            return video_schema.dump(video), 200


class UploadPhoto(Resource):
    def delete(self, id=None):
        if not id:
            abort(400, message='Bad Request: no id')
        try:
            db = db_session.create_session()
            photo = db.query(Photo).filter(Photo.id == id).first()
            db.delete(Photo)
        except BaseException as be:
            abort(500, message=f'Unexpected Error: {be}')
        else:
            db.commit()
            return {"photo_id": id}, 201

    def _get_photo_by_id(self, id):
        db = db_session.create_session()
        photo = db.query(Photo).filter(Photo.id == id).first()
        if photo is None:
            raise ValueError('no such video')
        return photo_schema.dump(photo)

    def _get_all_photos_by_id(self, owner_id):
        db = db_session.create_session()
        photos = db.query(Photo).filter(Photo.owner_id == owner_id).all()
        if photos is None or photos == []:
            raise ValueError("not found")
        photos_json = [photo_schema.dump(photo) for photo in photos]
        return photos_json

    def get(self, id=None):
        if not id:
            owner_id = request.args.get("owner_id")
            try:
                return self._get_all_photos_by_id(owner_id), 200
            except ValueError as ve:
                abort(404, message=f'ValueError: {ve}')
            except BaseException as be:
                abort(500, message=f'Unexpected error: {be}')

        try:
            return self._get_photo_by_id(id), 200
        except ValueError as ve:
            abort(404, message=f'ValueError: {ve}')
        except BaseException as be:
            abort(500, message=f'Unexpected error: {be}')

    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument(
            'photo',
            type=werkzeug.datastructures.FileStorage,
            location='files')
        parse.add_argument('owner_id', type=int)
        args = parse.parse_args()
        try:
            photo_file = args['photo']
            photo_uuid = uuid4()
            photo_filename = f"photo{photo_uuid}.{photo_file.content_type.split('/')[1]}"

            db = db_session.create_session()

            photo = Photo(filename=photo_filename)

            if args['owner_id']:
                volun = db.query(Volunteer).filter(
                    Volunteer.id == int(args['owner_id'])).first()
                if volun is None:
                    raise ValueError
                photo.owner = volun

            photo_file.save(os.path.join(PHOTOS_DIR, photo_filename))
            db.add(photo)
        except ValueError as ve:
            abort(400, message=f'ValueError: {ve}')
            db.rollback()
        except BaseException as be:
            abort(500, message=f'Unexpected Error: {be}')
            db.rollback()
        else:
            db.commit()
            return photo_schema.dump(photo), 200


class StatusResource(Resource):

    def delete(self, id=None):
        if not id:
            abort(400, message='Bad Request: no id')
        try:
            db = db_session.create_session()
            status = db.query(Status).filter(Status.id == id).first()
            db.delete(status)
        except BaseException as be:
            abort(500, message=f'Unexpected Error: {be}')
        else:
            db.commit()
            return {"status_id": id}, 201

    def patch(self, id=None):
        json = request.get_json()
        if not id:
            abort(400, message='Bad Request: no id')
        try:
            db = db_session.create_session()
            status = db.query(Status).filter(Status.id == id).first()
            if volunteer is None:
                raise ValueError

            for key in json:
                setattr(status, key, json[key])

            db.add(status)
            db.commit()
        except ValueError as ve:
            abort(400, message=f'ValueError: {ve}')
        except BaseException as be:
            abort(500, message=f'Unexpected Error: {be}')
        else:
            return {"status_id": status.id}, 201

        pass

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
            abort(500, message=f'Error: {ie}')
        except BaseException as be:
            abort(400, message=f'Bad Request: {be}')
        else:
            return {"status_id": status.id}, 201


class VolunteersResource(Resource):
    def delete(self, id=None):
        if not id:
            abort(400, message='Bad Request: no id')
        try:
            db = db_session.create_session()
            volunteer = db.query(Volunteer).filter(Volunteer.id == id).first()
            db.delete(volunteer)
        except BaseException as be:
            abort(500, message=f'Unexpected Error: {be}')
        else:
            db.commit()
            return {"volunteer_id": id}, 201

    def get(self, id=None):
        if not id:
            try:
                status_id = request.args.get('status_id')
                return self._get_all_volunteers(status_id), 200
            except ValueError as ve:
                abort(400, message=f'ValueError: {ve}')
                return
            except BaseException as be:
                abort(500, message=f'Unexpected Error: {be}')
                return

        try:
            return self._get_volunteer_by_id(id), 200
        except BaseException:
            abort(404, message='Volunteer not found')

    def _get_all_volunteers(self, status_id):
        db = db_session.create_session()
        if status_id:
            volunteers = db.query(Volunteer).filter(
                Volunteer.volunteer_status_id == status_id).all()
        else:
            volunteers = db.query(Volunteer).all()
        volunteers_json = [volunteer_schema.dump(
            volunteer) for volunteer in volunteers]
        return volunteers_json

    def _get_volunteer_by_id(self, volunteer_id):
        db = db_session.create_session()
        volunteer = db.query(Volunteer).filter(
            Volunteer.id == volunteer_id).first()
        if volunteer is None:
            raise ValueError('no such volunteer')
        volunteer_json = volunteer_schema.dump(volunteer)
        return volunteer_json

    def post(self):
        json = request.get_json()
        try:
            db = db_session.create_session()
            volunteer = volunteer_schema.load(json, session=db)
            db.add(volunteer)
            db.commit()
        except IntegrityError as ie:
            abort(500, message=f'Error: {ie}')
        except BaseException as be:
            abort(400, message=f'Bad Request; {be}')
        else:
            return {"volunteer_id": volunteer.id}, 201

    def patch(self, id=None):
        json = request.get_json()
        if not id:
            abort(400, message='Bad Request: no id')
        try:
            db = db_session.create_session()
            volunteer = db.query(Volunteer).filter(Volunteer.id == id).first()
            if volunteer is None:
                raise ValueError

            for key in json:
                setattr(volunteer, key, json[key])

            db.add(volunteer)
            db.commit()
            # print(json)
            # print(volunteer)

        except ValueError as ve:
            abort(400, message=f'ValueError: {ve}')
        except BaseException as be:
            abort(500, message=f'Unexpected Error: {be}')
        else:
            return {"volunteer_id": volunteer.id}, 201
