from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from db.photo import Photo


class PhotoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Photo
        load_instance = True
