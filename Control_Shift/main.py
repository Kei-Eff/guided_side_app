import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy


def create_app():

    app = Flask(__name__)

    app.config.from_object("config.app_config")

    db = SQLAlchemy(app)

    class Keyboard(db.Model):
        __tablename__ = "keyboards"
        keyboard_id = db.Column(db.Integer, primary_key=True)
        keyboard_name = db.Column(db.String(80), unique=True, nullable=False)

        def __init__(self, keyboard_name):
            self.keyboard_name = keyboard_name

        @property
        def serialize(self):
            return {
                "keyboard_id": self.keyboard_id,
                "keyboard_name": self.keyboard_name
            }

    db.create_all()



    @app.route("/")
    def homepage():
        return "Hello, world! Check this out!"

    @app.route("/keyboards/", methods=["GET"])
    def get_keyboards():
        keyboards = Keyboard.query.all()
        return jsonify([keyboard.serialize for keyboard in keyboards])

    @app.route("/keyboards/", methods=["POST"])
    def create_keeb():
        new_keeb = Keyboard(request.json['keyboard_name'])
        db.session.add(new_keeb)
        db.session.commit()
        return jsonify(new_keeb.serialize)

    @app.route("/keyboards/<int:id>/", methods=["GET"])
    def get_keyboard(id):
        keyboard = Keyboard.query.get_or_404(id)
        return jsonify(keyboard.serialize)

    @app.route("/keyboards/<int:id>/", methods=["PUT", "PATCH"])
    def update_keyboard(id):
        keyboard = Keyboard.query.filter_by(keyboard_id=id)
        keyboard.update(dict(keyboard_name=request.json["keyboard_name"]))
        db.session.commit()
        return jsonify(keyboard.first().serialize)

    @app.route("/keyboards/<int:id>/", methods=["DELETE"])
    def delete_keyboard(id):
        keyboard = Keyboard.query.get_or_404(id)
        db.session.delete(keyboard)
        db.session.commit()
        return jsonify(keyboard.serialize)


    return app