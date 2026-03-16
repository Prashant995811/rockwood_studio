from flask import Blueprint, flash, redirect, render_template, request, url_for
from sqlalchemy import or_

from app.extensions import db
from app.forms import ContactForm
from app.models import ContactInquiry, GalleryImage, Project, Service, Testimonial
from app.utils.helpers import get_settings, send_contact_to_formspree


public_bp = Blueprint("public", __name__)


@public_bp.app_context_processor
def inject_site_settings():
    return {"site_settings": get_settings()}


@public_bp.route("/")
def home():
    featured_services = (
        Service.query.filter_by(is_featured=True)
        .order_by(Service.created_at.desc())
        .limit(6)
        .all()
    )
    featured_projects = (
        Project.query.filter_by(is_featured=True)
        .order_by(Project.created_at.desc())
        .limit(6)
        .all()
    )
    testimonials = (
        Testimonial.query.filter_by(is_featured=True)
        .order_by(Testimonial.created_at.desc())
        .limit(3)
        .all()
    )
    return render_template(
        "home.html",
        title="Home",
        featured_services=featured_services,
        featured_projects=featured_projects,
        testimonials=testimonials,
    )


@public_bp.route("/about")
def about():
    return render_template("about.html", title="About Us")


@public_bp.route("/services")
def services():
    all_services = Service.query.order_by(Service.title.asc()).all()
    return render_template("services.html", title="Services", services=all_services)


@public_bp.route("/projects")
def projects():
    category = request.args.get("category", "").strip()
    search = request.args.get("search", "").strip()

    query = Project.query
    if category:
        query = query.filter(Project.category == category)
    if search:
        like_value = f"%{search}%"
        query = query.filter(
            or_(
                Project.title.ilike(like_value),
                Project.category.ilike(like_value),
                Project.location.ilike(like_value),
            )
        )

    all_projects = query.order_by(Project.created_at.desc()).all()
    categories = [
        row[0]
        for row in db.session.query(Project.category)
        .distinct()
        .order_by(Project.category.asc())
    ]

    return render_template(
        "projects.html",
        title="Projects",
        projects=all_projects,
        categories=categories,
        active_category=category,
        search_query=search,
    )


@public_bp.route("/projects/<slug>")
def project_detail(slug):
    project = Project.query.filter_by(slug=slug).first_or_404()
    return render_template("project_detail.html", title=project.title, project=project)


@public_bp.route("/gallery")
def gallery():
    images = GalleryImage.query.order_by(GalleryImage.created_at.desc()).all()
    return render_template("gallery.html", title="Gallery", images=images)


@public_bp.route("/testimonials")
def testimonials():
    all_testimonials = Testimonial.query.order_by(Testimonial.created_at.desc()).all()
    return render_template(
        "testimonials.html",
        title="Testimonials",
        testimonials=all_testimonials,
    )


@public_bp.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        inquiry = ContactInquiry(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            subject=form.subject.data,
            message=form.message.data,
        )
        db.session.add(inquiry)
        db.session.commit()

        success, status_message = send_contact_to_formspree(
            {
                "name": form.name.data,
                "email": form.email.data,
                "phone": form.phone.data,
                "subject": form.subject.data,
                "message": form.message.data,
            }
        )

        if success:
            flash("Your message has been sent successfully.", "success")
        else:
            flash(
                "Your inquiry was saved, but email forwarding could not be completed right now. "
                + status_message,
                "warning",
            )

        return redirect(url_for("public.contact"))

    return render_template("contact.html", title="Contact Us", form=form)
