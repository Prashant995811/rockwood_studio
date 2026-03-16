from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db


class TimestampMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )


class AdminUser(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Service(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(160), unique=True, nullable=False)
    short_description = db.Column(db.String(255), nullable=False)
    full_description = db.Column(db.Text, nullable=False)
    image_filename = db.Column(db.String(255))
    is_featured = db.Column(db.Boolean, default=False, nullable=False)


class Project(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(160), unique=True, nullable=False)
    category = db.Column(db.String(120), nullable=False)
    short_description = db.Column(db.String(255), nullable=False)
    full_description = db.Column(db.Text, nullable=False)
    image_filename = db.Column(db.String(255))
    completion_date = db.Column(db.Date)
    location = db.Column(db.String(150))
    is_featured = db.Column(db.Boolean, default=False, nullable=False)


class GalleryImage(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    image_filename = db.Column(db.String(255), nullable=False)
    alt_text = db.Column(db.String(255))


class Testimonial(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(120), nullable=False)
    review = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False, default=5)
    is_featured = db.Column(db.Boolean, default=False, nullable=False)


class ContactInquiry(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(30))
    subject = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(30), nullable=False, default="New")


class SiteSetting(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(150), nullable=False, default="Rockwood Studio")
    logo_filename = db.Column(db.String(255), default="")
    tagline = db.Column(
        db.String(255),
        nullable=False,
        default="Elegant interior design and complete interior work solutions",
    )
    contact_email = db.Column(
        db.String(120),
        nullable=False,
        default="hello@rockwoodstudio.com",
    )
    phone = db.Column(db.String(50), nullable=False, default="+91 98765 43210")
    address = db.Column(
        db.String(255),
        nullable=False,
        default="Your studio address goes here",
    )
    hero_title = db.Column(
        db.String(255),
        nullable=False,
        default="Interior spaces designed with warmth, detail, and purpose.",
    )
    hero_subtitle = db.Column(
        db.Text,
        nullable=False,
        default="We create premium residential and commercial interiors that blend function, comfort, and timeless style.",
    )
    footer_text = db.Column(
        db.String(255),
        nullable=False,
        default="Rockwood Studio crafts interior experiences with care and clarity.",
    )
    facebook_url = db.Column(db.String(255), default="")
    instagram_url = db.Column(db.String(255), default="")
    linkedin_url = db.Column(db.String(255), default="")
    youtube_url = db.Column(db.String(255), default="")
    map_embed_url = db.Column(
        db.Text,
        default="https://www.google.com/maps?q=New+Delhi&output=embed",
    )
