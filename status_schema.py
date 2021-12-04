from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from db.status import Status

class StatusSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Status
        load_instance = True
