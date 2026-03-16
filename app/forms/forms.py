from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import (
    BooleanField,
    DateField,
    IntegerField,
    PasswordField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional, URL


IMAGE_TYPES = ["jpg", "jpeg", "png", "webp"]


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=80)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class ServiceForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=150)])
    short_description = StringField(
        "Short Description", validators=[DataRequired(), Length(max=255)]
    )
    full_description = TextAreaField("Full Description", validators=[DataRequired()])
    image = FileField(
        "Service Image",
        validators=[Optional(), FileAllowed(IMAGE_TYPES, "Image files only.")],
    )
    is_featured = BooleanField("Show on homepage")
    submit = SubmitField("Save Service")


class ProjectForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=150)])
    category = StringField("Category", validators=[DataRequired(), Length(max=120)])
    short_description = StringField(
        "Short Description", validators=[DataRequired(), Length(max=255)]
    )
    full_description = TextAreaField("Full Description", validators=[DataRequired()])
    location = StringField("Location", validators=[Optional(), Length(max=150)])
    completion_date = DateField(
        "Completion Date", validators=[Optional()], format="%Y-%m-%d"
    )
    image = FileField(
        "Project Image",
        validators=[Optional(), FileAllowed(IMAGE_TYPES, "Image files only.")],
    )
    is_featured = BooleanField("Show on homepage")
    submit = SubmitField("Save Project")


class GalleryForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=150)])
    alt_text = StringField("Alt Text", validators=[Optional(), Length(max=255)])
    image = FileField(
        "Gallery Image",
        validators=[DataRequired(), FileAllowed(IMAGE_TYPES, "Image files only.")],
    )
    submit = SubmitField("Save Image")


class TestimonialForm(FlaskForm):
    client_name = StringField(
        "Client Name", validators=[DataRequired(), Length(max=120)]
    )
    review = TextAreaField("Review", validators=[DataRequired()])
    rating = IntegerField(
        "Rating", validators=[DataRequired(), NumberRange(min=1, max=5)]
    )
    is_featured = BooleanField("Show on homepage")
    submit = SubmitField("Save Testimonial")


class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=120)])
    email = StringField(
        "Email", validators=[DataRequired(), Email(), Length(max=120)]
    )
    phone = StringField("Phone", validators=[Optional(), Length(max=30)])
    subject = StringField("Subject", validators=[DataRequired(), Length(max=150)])
    message = TextAreaField("Message", validators=[DataRequired(), Length(min=10)])
    submit = SubmitField("Send Message")


class SettingsForm(FlaskForm):
    logo = FileField(
        "Website Logo",
        validators=[Optional(), FileAllowed(IMAGE_TYPES, "Image files only.")],
    )
    company_name = StringField(
        "Company Name", validators=[DataRequired(), Length(max=150)]
    )
    tagline = StringField("Tagline", validators=[DataRequired(), Length(max=255)])
    contact_email = StringField(
        "Contact Email", validators=[DataRequired(), Email(), Length(max=120)]
    )
    phone = StringField("Phone", validators=[DataRequired(), Length(max=50)])
    address = StringField("Address", validators=[DataRequired(), Length(max=255)])
    hero_title = StringField(
        "Hero Title", validators=[DataRequired(), Length(max=255)]
    )
    hero_subtitle = TextAreaField("Hero Subtitle", validators=[DataRequired()])
    footer_text = StringField(
        "Footer Text", validators=[DataRequired(), Length(max=255)]
    )
    facebook_url = StringField("Facebook URL", validators=[Optional(), URL()])
    instagram_url = StringField("Instagram URL", validators=[Optional(), URL()])
    linkedin_url = StringField("LinkedIn URL", validators=[Optional(), URL()])
    youtube_url = StringField("YouTube URL", validators=[Optional(), URL()])
    map_embed_url = TextAreaField(
        "Google Map Embed URL", validators=[Optional(), URL()]
    )
    submit = SubmitField("Save Settings")
