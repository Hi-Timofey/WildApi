from sqlalchemy import Column
from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean
from sqlalchemy import orm


from .db_session import SqlAlchemyBase

class Status(SqlAlchemyBase):
    __tablename__ = 'statuses'

    id = Column('status_id', Integer,
                        primary_key=True, autoincrement=True, unique=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    volunteers_with_status = orm.relation('Volunteer', back_populates='volunteer_status')


# class StatusSchema(SQLAlchemyAutoSchema):
#     class Meta:
#         model = Status
#         load_instance = True
