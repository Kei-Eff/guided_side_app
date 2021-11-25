from flask import Blueprint, jsonify, request, render_template, redirect, url_for, abort, current_app
from main import db
from models.keyboards import Keyboard
from schemas.keyboard_schema import keyboard_schema, keyboards_schema
from flask_login import login_required, current_user
import boto3

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
@login_required
def create_keeb():
    new_keeb = keyboard_schema.load(request.form)
    new_keeb.creator = current_user
    db.session.add(new_keeb)
    db.session.commit()
    return redirect(url_for("keyboards.get_keyboards"))


@keyboards.route("/keyboards/<int:id>/", methods=["GET"])
def get_keyboard(id):
    keyboard = Keyboard.query.get_or_404(id)

    s3_client=boto3.client("s3")
    bucket_name=current_app.config["AWS_S3_BUCKET"]
    image_url = s3_client.generate_presigned_url(
        'get_object',
        Params={
            "Bucket": bucket_name,
            "Key": keyboard.image_filename
        },
        ExpiresIn=100
    )

    data = {
        "page_title": "Keyboard Detail",
        "keyboard": keyboard_schema.dump(keyboard),
        "image": image_url
    }
    return render_template("keyboard_detail.html", page_data=data)


@keyboards.route("/keyboards/<int:id>/", methods=["POST"])
@login_required
def update_keyboard(id):
    keyboard = Keyboard.query.filter_by(keyboard_id=id)
    
    if current_user.id != keyboard.first().creator_id:
        abort(403, "You do not have permission to alter this keyboard.")

    updated_fields = keyboard_schema.dump(request.form)
    if updated_fields:
        keyboard.update(updated_fields)
    db.session.commit()

    data = {
        "page_title": "Keyboard Index",
        "keyboards": keyboard_schema.dump(keyboards.first())
    }
    return render_template("keyboard_index.html", page_data=data)

@keyboards.route("/keyboards/<int:id>/enrol/", methods=["POST"])
@login_required
def enrol_keyboard(id):
    keyboard = Keyboard.query.get_or_404(id)
    keyboard.owners.append(current_user)
    db.session.commit()
    return redirect(url_for('users.user_detail'))

@keyboards.route("/keyboards/<int:id>/drop/", methods=["POST"])
@login_required
def drop_keyboard(id):
    keyboard = Keyboard.query.get_or_404(id)
    keyboard.owners.remove(current_user)
    db.session.commit()
    return redirect(url_for("users.user_detail"))


@keyboards.route("/keyboards/<int:id>/delete/", methods=["POST"])
@login_required
def delete_keyboard(id):
    keyboard = Keyboard.query.get_or_404(id)

    if current_user.id != keyboard.creator_id:
        abort(403, "You do not have persmission to delete this keyboard.")
        
    db.session.delete(keyboard)
    db.session.commit()
    return redirect(url_for("keyboards.get_keyboards"))