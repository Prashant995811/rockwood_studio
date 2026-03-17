from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.extensions import db
from app.forms import (
    GalleryForm,
    LoginForm,
    ProjectForm,
    ServiceForm,
    SettingsForm,
    TestimonialForm,
)
from app.models import AdminUser, ContactInquiry, GalleryImage, Project, Service, Testimonial
from app.utils.decorators import admin_required
from app.utils.helpers import delete_image_file, get_settings, save_image, unique_slug


admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("admin_user_id"):
        return redirect(url_for("admin.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        admin_user = AdminUser.query.filter_by(username=form.username.data).first()
        if admin_user and admin_user.check_password(form.password.data):
            session["admin_user_id"] = admin_user.id
            flash("Welcome back to the admin panel.", "success")
            return redirect(url_for("admin.dashboard"))
        flash("Invalid username or password.", "danger")
    return render_template("admin/login.html", title="Admin Login", form=form)


@admin_bp.route("/logout")
@admin_required
def logout():
    session.pop("admin_user_id", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("rrrrrrrrr.login"))


@admin_bp.route("/")
@admin_required
def dashboard():
    stats = {
        "services": Service.query.count(),
        "projects": Project.query.count(),
        "gallery": GalleryImage.query.count(),
        "testimonials": Testimonial.query.count(),
        "inquiries": ContactInquiry.query.count(),
    }
    recent_inquiries = (
        ContactInquiry.query.order_by(ContactInquiry.created_at.desc()).limit(5).all()
    )
    return render_template(
        "admin/dashboard.html",
        title="Dashboard",
        stats=stats,
        recent_inquiries=recent_inquiries,
    )


@admin_bp.route("/services")
@admin_required
def services():
    all_services = Service.query.order_by(Service.created_at.desc()).all()
    return render_template(
        "admin/services_list.html", title="Manage Services", services=all_services
    )


@admin_bp.route("/services/create", methods=["GET", "POST"])
@admin_required
def create_service():
    form = ServiceForm()
    if form.validate_on_submit():
        service = Service(
            title=form.title.data,
            slug=unique_slug(Service, form.title.data),
            short_description=form.short_description.data,
            full_description=form.full_description.data,
            image_filename=save_image(form.image.data),
            is_featured=form.is_featured.data,
        )
        db.session.add(service)
        db.session.commit()
        flash("Service created successfully.", "success")
        return redirect(url_for("admin.services"))
    return render_template(
        "admin/service_form.html", title="Add Service", form=form, service=None
    )


@admin_bp.route("/services/<int:service_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_service(service_id):
    service = Service.query.get_or_404(service_id)
    form = ServiceForm(obj=service)
    if form.validate_on_submit():
        service.title = form.title.data
        service.slug = unique_slug(Service, form.title.data, service.id)
        service.short_description = form.short_description.data
        service.full_description = form.full_description.data
        if form.image.data:
            delete_image_file(service.image_filename)
            service.image_filename = save_image(form.image.data)
        service.is_featured = form.is_featured.data
        db.session.commit()
        flash("Service updated successfully.", "success")
        return redirect(url_for("admin.services"))
    return render_template(
        "admin/service_form.html", title="Edit Service", form=form, service=service
    )


@admin_bp.route("/services/<int:service_id>/delete", methods=["POST"])
@admin_required
def delete_service(service_id):
    service = Service.query.get_or_404(service_id)
    delete_image_file(service.image_filename)
    db.session.delete(service)
    db.session.commit()
    flash("Service deleted successfully.", "info")
    return redirect(url_for("admin.services"))


@admin_bp.route("/services/<int:service_id>/delete-image", methods=["POST"])
@admin_required
def delete_service_image(service_id):
    service = Service.query.get_or_404(service_id)
    if service.image_filename:
        delete_image_file(service.image_filename)
        service.image_filename = None
        db.session.commit()
        flash("Service image removed successfully.", "success")
    else:
        flash("This service does not have an image to remove.", "warning")
    return redirect(url_for("admin.edit_service", service_id=service.id))


@admin_bp.route("/projects")
@admin_required
def projects():
    all_projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template(
        "admin/projects_list.html", title="Manage Projects", projects=all_projects
    )


@admin_bp.route("/projects/create", methods=["GET", "POST"])
@admin_required
def create_project():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(
            title=form.title.data,
            slug=unique_slug(Project, form.title.data),
            category=form.category.data,
            short_description=form.short_description.data,
            full_description=form.full_description.data,
            location=form.location.data,
            completion_date=form.completion_date.data,
            image_filename=save_image(form.image.data),
            is_featured=form.is_featured.data,
        )
        db.session.add(project)
        db.session.commit()
        flash("Project created successfully.", "success")
        return redirect(url_for("admin.projects"))
    return render_template(
        "admin/project_form.html", title="Add Project", form=form, project=None
    )


@admin_bp.route("/projects/<int:project_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)
    form = ProjectForm(obj=project)
    if form.validate_on_submit():
        project.title = form.title.data
        project.slug = unique_slug(Project, form.title.data, project.id)
        project.category = form.category.data
        project.short_description = form.short_description.data
        project.full_description = form.full_description.data
        project.location = form.location.data
        project.completion_date = form.completion_date.data
        if form.image.data:
            delete_image_file(project.image_filename)
            project.image_filename = save_image(form.image.data)
        project.is_featured = form.is_featured.data
        db.session.commit()
        flash("Project updated successfully.", "success")
        return redirect(url_for("admin.projects"))
    return render_template(
        "admin/project_form.html", title="Edit Project", form=form, project=project
    )


@admin_bp.route("/projects/<int:project_id>/delete", methods=["POST"])
@admin_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    delete_image_file(project.image_filename)
    db.session.delete(project)
    db.session.commit()
    flash("Project deleted successfully.", "info")
    return redirect(url_for("admin.projects"))


@admin_bp.route("/projects/<int:project_id>/delete-image", methods=["POST"])
@admin_required
def delete_project_image(project_id):
    project = Project.query.get_or_404(project_id)
    if project.image_filename:
        delete_image_file(project.image_filename)
        project.image_filename = None
        db.session.commit()
        flash("Project image removed successfully.", "success")
    else:
        flash("This project does not have an image to remove.", "warning")
    return redirect(url_for("admin.edit_project", project_id=project.id))


@admin_bp.route("/gallery")
@admin_required
def gallery():
    images = GalleryImage.query.order_by(GalleryImage.created_at.desc()).all()
    return render_template("admin/gallery_list.html", title="Manage Gallery", images=images)


@admin_bp.route("/gallery/create", methods=["GET", "POST"])
@admin_required
def create_gallery_image():
    form = GalleryForm()
    if form.validate_on_submit():
        image = GalleryImage(
            title=form.title.data,
            alt_text=form.alt_text.data,
            image_filename=save_image(form.image.data),
        )
        db.session.add(image)
        db.session.commit()
        flash("Gallery image added successfully.", "success")
        return redirect(url_for("admin.gallery"))
    return render_template("admin/gallery_form.html", title="Add Gallery Image", form=form)


@admin_bp.route("/gallery/<int:image_id>/delete", methods=["POST"])
@admin_required
def delete_gallery_image(image_id):
    image = GalleryImage.query.get_or_404(image_id)
    delete_image_file(image.image_filename)
    db.session.delete(image)
    db.session.commit()
    flash("Gallery image deleted successfully.", "info")
    return redirect(url_for("admin.gallery"))


@admin_bp.route("/testimonials")
@admin_required
def testimonials():
    all_testimonials = Testimonial.query.order_by(Testimonial.created_at.desc()).all()
    return render_template(
        "admin/testimonials_list.html",
        title="Manage Testimonials",
        testimonials=all_testimonials,
    )


@admin_bp.route("/testimonials/create", methods=["GET", "POST"])
@admin_required
def create_testimonial():
    form = TestimonialForm()
    if form.validate_on_submit():
        testimonial = Testimonial(
            client_name=form.client_name.data,
            review=form.review.data,
            rating=form.rating.data,
            is_featured=form.is_featured.data,
        )
        db.session.add(testimonial)
        db.session.commit()
        flash("Testimonial added successfully.", "success")
        return redirect(url_for("admin.testimonials"))
    return render_template(
        "admin/testimonial_form.html",
        title="Add Testimonial",
        form=form,
        testimonial=None,
    )


@admin_bp.route("/testimonials/<int:testimonial_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_testimonial(testimonial_id):
    testimonial = Testimonial.query.get_or_404(testimonial_id)
    form = TestimonialForm(obj=testimonial)
    if form.validate_on_submit():
        testimonial.client_name = form.client_name.data
        testimonial.review = form.review.data
        testimonial.rating = form.rating.data
        testimonial.is_featured = form.is_featured.data
        db.session.commit()
        flash("Testimonial updated successfully.", "success")
        return redirect(url_for("admin.testimonials"))
    return render_template(
        "admin/testimonial_form.html",
        title="Edit Testimonial",
        form=form,
        testimonial=testimonial,
    )


@admin_bp.route("/testimonials/<int:testimonial_id>/delete", methods=["POST"])
@admin_required
def delete_testimonial(testimonial_id):
    testimonial = Testimonial.query.get_or_404(testimonial_id)
    db.session.delete(testimonial)
    db.session.commit()
    flash("Testimonial deleted successfully.", "info")
    return redirect(url_for("admin.testimonials"))


@admin_bp.route("/inquiries")
@admin_required
def inquiries():
    all_inquiries = ContactInquiry.query.order_by(ContactInquiry.created_at.desc()).all()
    return render_template(
        "admin/inquiries_list.html", title="Contact Inquiries", inquiries=all_inquiries
    )


@admin_bp.route("/inquiries/<int:inquiry_id>/status", methods=["POST"])
@admin_required
def update_inquiry_status(inquiry_id):
    inquiry = ContactInquiry.query.get_or_404(inquiry_id)
    inquiry.status = request.form.get("status", inquiry.status)
    db.session.commit()
    flash("Inquiry status updated.", "success")
    return redirect(url_for("admin.inquiries"))


@admin_bp.route("/settings", methods=["GET", "POST"])
@admin_required
def settings():
    site_settings = get_settings()
    form = SettingsForm(obj=site_settings)
    if form.validate_on_submit():
        site_settings.company_name = form.company_name.data
        site_settings.tagline = form.tagline.data
        site_settings.contact_email = form.contact_email.data
        site_settings.phone = form.phone.data
        site_settings.address = form.address.data
        site_settings.hero_title = form.hero_title.data
        site_settings.hero_subtitle = form.hero_subtitle.data
        site_settings.footer_text = form.footer_text.data
        site_settings.facebook_url = form.facebook_url.data
        site_settings.instagram_url = form.instagram_url.data
        site_settings.linkedin_url = form.linkedin_url.data
        site_settings.youtube_url = form.youtube_url.data
        site_settings.map_embed_url = form.map_embed_url.data
        if form.logo.data:
            delete_image_file(site_settings.logo_filename)
            site_settings.logo_filename = save_image(form.logo.data)
        db.session.commit()
        flash("Website settings updated successfully.", "success")
        return redirect(url_for("admin.settings"))
    return render_template(
        "admin/settings_form.html",
        title="Website Settings",
        form=form,
        site_settings=site_settings,
    )


@admin_bp.route("/settings/delete-logo", methods=["POST"])
@admin_required
def delete_logo():
    site_settings = get_settings()
    if site_settings.logo_filename:
        delete_image_file(site_settings.logo_filename)
        site_settings.logo_filename = ""
        db.session.commit()
        flash("Website logo removed successfully.", "success")
    else:
        flash("No logo is currently uploaded.", "warning")
    return redirect(url_for("admin.settings"))
