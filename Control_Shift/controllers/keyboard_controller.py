from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from main import db
from models.keyboards import Keyboard
from schemas.keyboard_schema import keyboard_schema, keyboards_schema

keyboards = Blueprint('keyboards', __name__)

@keyboards.route("/")
def homepage():
    data = {
        "page_title": "Homepage"
    }

    return render_template("homepage.html", page_data=data)


@keyboards.route("/keyboards/", methods=["GET"])
def get_keyboards():
    keyboards = Keyboard.query.all()
    data = {
        "page_title": "Keyboard Index",
        "keyboards": keyboard_schema.dump(keyboards)
    }
    return render_template("keyboard_index.html", page_data=data)


# The POST route endpoint
@keyboards.route("/keyboards/", methods=["POST"])
def create_keeb():
    new_keeb = keyboard_schema.load(request.form)
    db.session.add(new_keeb)
    db.session.commit()
    return redirect(url_for("keyboards.get_keyboards"))


@keyboards.route("/keyboards/<int:id>/", methods=["GET"])
def get_keyboard(id):
    keyboard = Keyboard.query.get_or_404(id)
    data = {
        "page_title": "Keyboard Detail",
        "keyboard": keyboard_schema. dump(keyboard)
    }
    return render_template("keyboard_detail.html", page_data=data)


@keyboards.route("/keyboards/<int:id>/", methods=["POST"])
def update_keyboard(id):
    keyboard = Keyboard.query.filter_by(keyboard_id=id)
    

    updated_fields = keyboard_schema.dump(request.form)
    if updated_fields:
        keyboard.update(updated_fields)
    db.session.commit()

    data = {
        "page_title": "Keyboard Index",
        "keyboards": keyboard_schema.dump(keyboards.first())
    }
    return render_template("keyboard_index.html", page_data=data)


@keyboards.route("/keyboards/<int:id>/delete", methods=["POST"])
def delete_keyboard(id):
    keyboard = Keyboard.query.get_or_404(id)
    db.session.delete(keyboard)
    db.session.commit()
    return redirect(url_for("keyboards.get_keyboards"))