from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from db.video import Video


class VideoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Video
        load_instance = True
