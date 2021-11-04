from flask import Blueprint, jsonify, request
from main import db
from models.keyboards import Keyboard
from schemas.keyboard_schema import keyboard_schema, keyboards_schema

keyboards = Blueprint('keyboards', __name__)

@keyboards.route("/")
def homepage():
    return "Hello, world! Check this out!"

@keyboards.route("/keyboards/", methods=["GET"])
def get_keyboards():
    keyboards = Keyboard.query.all()
    return jsonify(keyboards_schema.dump(keyboards))

@keyboards.route("/keyboards/", methods=["POST"])
def create_keeb():
    new_keeb = keyboard_schema.load(request.json)
    db.session.add(new_keeb)
    db.session.commit()
    return jsonify(keyboard_schema.dump(new_keeb))

@keyboards.route("/keyboards/<int:id>/", methods=["GET"])
def get_keyboard(id):
    keyboard = Keyboard.query.get_or_404(id)
    return jsonify(keyboard_schema.dump(keyboard))

@keyboards.route("/keyboards/<int:id>/", methods=["PUT", "PATCH"])
def update_keyboard(id):
    keyboard = Keyboard.query.filter_by(keyboard_id=id)
    
    updated_fields = keybaord_schema.dump(request.json)
    if updated_fields:
        keyboard.update(updated_fields)
    db.session.commit()
    return jsonify(keyboard_schema.dump(keyboard.first()))

@keyboards.route("/keyboards/<int:id>/", methods=["DELETE"])
def delete_keyboard(id):
    keyboard = Keyboard.query.get_or_404(id)
    db.session.delete(keyboard)
    db.session.commit()
    return jsonify(keyboard_schema.dump(keyboard))