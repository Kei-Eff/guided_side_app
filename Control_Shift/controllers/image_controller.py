from flask import Blueprint, request, redirect, abort, url_for, current_app
from pathlib import Path
from models.keyboards import Keyboard
import boto3

keyboard_images = Blueprint('keyboard_images', __name__)

@keyboard_images.route("/keyboards/<int:id>/image/", methods=["POST"])
def update_image(id):
    keyboard = Keyboard.query.get_or_404(id)
    if "image" in request.files:
        image = request.files["image"]
        if Path(image.filename).suffix != ".png":
            return abort(400, description="Invalid file type")

        bucket = boto3.resource("s3").Bucket(current_app.config["AWS_S3_BUCKET"])
        bucket.upload_fileobj(image, keyboard.image_filename)


        return redirect(url_for("keyboards.get_keyboard", id=id))

    return abort(400, description="No image")