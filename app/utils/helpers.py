import os
import uuid
from pathlib import Path

import requests
from flask import current_app
from slugify import slugify
from werkzeug.utils import secure_filename

from app.extensions import db
from app.models import SiteSetting


def save_image(file_storage):
    if not file_storage or not file_storage.filename:
        return None

    upload_folder = Path(current_app.config["UPLOAD_FOLDER"])
    upload_folder.mkdir(parents=True, exist_ok=True)

    original_name = secure_filename(file_storage.filename)
    extension = os.path.splitext(original_name)[1].lower()
    filename = f"{uuid.uuid4().hex}{extension}"
    file_storage.save(upload_folder / filename)
    return filename


def delete_image_file(filename):
    if not filename:
        return

    file_path = Path(current_app.config["UPLOAD_FOLDER"]) / filename
    if file_path.exists() and file_path.is_file():
        file_path.unlink()


def unique_slug(model_class, title, current_id=None):
    base_slug = slugify(title)
    slug = base_slug
    counter = 2

    while True:
        query = model_class.query.filter_by(slug=slug)
        if current_id:
            query = query.filter(model_class.id != current_id)
        if not query.first():
            return slug
        slug = f"{base_slug}-{counter}"
        counter += 1


def get_settings():
    settings = SiteSetting.query.first()
    if not settings:
        settings = SiteSetting()
        db.session.add(settings)
        db.session.commit()
    return settings


def send_contact_to_formspree(data):
    endpoint = current_app.config.get("FORMSPREE_ENDPOINT")
    if not endpoint:
        return False, "Formspree endpoint is not configured."

    payload = {
        "name": data["name"],
        "email": data["email"],
        "phone": data["phone"],
        "subject": data["subject"],
        "message": data["message"],
    }

    try:
        response = requests.post(endpoint, data=payload, timeout=10)
        if response.ok:
            return True, "Message sent successfully."
        return False, "Formspree request failed."
    except requests.RequestException:
        return False, "Unable to reach Formspree right now."
