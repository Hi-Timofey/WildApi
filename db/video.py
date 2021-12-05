import datetime
from sqlalchemy import Column
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy import orm


from .db_session import SqlAlchemyBase


class Video(SqlAlchemyBase):
    __tablename__ = 'videos'

    id = Column('video_id', Integer,
                primary_key=True, autoincrement=True, unique=True)
    filename = Column(String, nullable=False)
    upload_time = Column(DateTime, default=datetime.datetime.utcnow)

    owner_id = Column(Integer, ForeignKey("volunteers.volunteer_id"))
    owner = orm.relation('Volunteer', back_populates='video')
