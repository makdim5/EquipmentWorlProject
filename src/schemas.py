from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from src.models import UchetCompOborud


class EquipmentSchema(SQLAlchemyAutoSchema):

    class Meta:
        model = UchetCompOborud
        load_instance = True
