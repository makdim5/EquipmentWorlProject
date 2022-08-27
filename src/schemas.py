from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from src.models import UchetCompOborud, EternalNumbers


class EquipmentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UchetCompOborud
        load_instance = True


class EternalNumbersSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = EternalNumbers
        load_instance = True
