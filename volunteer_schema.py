from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from db.volunteer import Volunteer

class VolunteerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Volunteer
        load_instance = True
        include_relationships = True
        include_fk = True
