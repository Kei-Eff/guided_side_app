from flask import Blueprint, jsonify, request
from main import db
from models.keyboards import Keyboard

keyboards = Blueprint('keyboards', __name__)

@keyboards.route("/")
def homepage():
    return "Hello, world! Check this out!"

@keyboards.route("/keyboards/", methods=["GET"])
def get_keyboards():
    keyboards = Keyboard.query.all()
    return jsonify([keyboard.serialize for keyboard in keyboards])

@keyboards.route("/keyboards/", methods=["POST"])
def create_keeb():
    new_keeb = Keyboard(request.json['keyboard_name'])
    db.session.add(new_keeb)
    db.session.commit()
    return jsonify(new_keeb.serialize)

@keyboards.route("/keyboards/<int:id>/", methods=["GET"])
def get_keyboard(id):
    keyboard = Keyboard.query.get_or_404(id)
    return jsonify(keyboard.serialize)

@keyboards.route("/keyboards/<int:id>/", methods=["PUT", "PATCH"])
def update_keyboard(id):
    keyboard = Keyboard.query.filter_by(keyboard_id=id)
    keyboard.update(dict(keyboard_name=request.json["keyboard_name"]))
    db.session.commit()
    return jsonify(keyboard.first().serialize)

@keyboards.route("/keyboards/<int:id>/", methods=["DELETE"])
def delete_keyboard(id):
    keyboard = Keyboard.query.get_or_404(id)
    db.session.delete(keyboard)
    db.session.commit()
    return jsonify(keyboard.serialize)