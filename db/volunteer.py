from sqlalchemy import Column
from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean
from sqlalchemy import orm

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from .db_session import SqlAlchemyBase

class Volunteer(SqlAlchemyBase):
    __tablename__ = 'volunteers'

    id = Column('volunteer_id', Integer, primary_key=True)

    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    patronymic = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)

    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    link = Column(String, nullable=False)

    address = Column(String, nullable=False)

    education = Column(String, nullable=False)
    sphere = Column(String, nullable=False)
    experience = Column(String)
    recommendations = Column(String)
    volunteer_book = Column(Boolean, nullable=False)


    travel_place = Column(String, nullable=False)
    target_place = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    motivation_letter = Column(String)

    comment = Column(String)


class VolunteerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Volunteer
        load_instance = True

'''
    id = Integer

    name = String
    surname = String
    patronymic = String
    birth_date = Date

    email = String
    phone = String
    link = String

    address = String

    education = String
    sphere = String
    experience = String
    recommendations = String
    volunteer_book = Boolean


    travel_place = String
    target_place = String
    start_date = Date
    end_date = Date

    motivation_letter = String

    comment = String
'''
