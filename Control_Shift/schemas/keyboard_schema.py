from main import ma
from models.keyboards import Keyboard
from marshmallow_sqlalchemy import auto_field
from marshmallow.validate import Length

class KeyboardSchema(ma.SQLAlchemyAutoSchema):
    keyboard_id = auto_field(dump_only=True)
    keyboard_name = auto_field(required=True, validate=Length(min=1))

    class Meta:
        model = Keyboard
        load_instance = True

keyboard_schema = KeyboardSchema()
keyboards_schema = KeyboardSchema(many=True)