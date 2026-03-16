from config import Config

from app.extensions import db
from app.models import AdminUser, Project, Service, SiteSetting, Testimonial
from app.utils.helpers import unique_slug


def ensure_default_admin():
    admin = AdminUser.query.first()
    if admin:
        return

    admin = AdminUser(username=Config.DEFAULT_ADMIN_USERNAME)
    admin.set_password(Config.DEFAULT_ADMIN_PASSWORD)
    db.session.add(admin)
    db.session.commit()


def ensure_default_settings():
    settings = SiteSetting.query.first()
    if settings:
        return

    settings = SiteSetting()
    db.session.add(settings)

    if Service.query.count() == 0:
        sample_services = [
            ("Modular Kitchen", "Smart kitchen layouts with elegant finishes."),
            ("Wardrobe Design", "Custom wardrobes built for storage and style."),
            ("Living Room Interior", "Balanced living spaces with warm, modern details."),
            ("Office Interior", "Professional workspaces designed for function and comfort."),
        ]
        for title, desc in sample_services:
            db.session.add(
                Service(
                    title=title,
                    slug=unique_slug(Service, title),
                    short_description=desc,
                    full_description=f"{desc} We tailor each project around your needs, your space, and your preferred design language.",
                    is_featured=True,
                )
            )

    if Project.query.count() == 0:
        sample_projects = [
            (
                "Urban Kitchen Retreat",
                "Modular Kitchen",
                "A warm, efficient kitchen renovation.",
                "Gurugram",
            ),
            (
                "The Calm Bedroom",
                "Bedroom Interior",
                "A soft-toned bedroom with custom storage.",
                "Noida",
            ),
            (
                "Studio Work Hub",
                "Office Interior",
                "A compact office designed for focus and flow.",
                "Delhi",
            ),
        ]
        for title, category, desc, location in sample_projects:
            db.session.add(
                Project(
                    title=title,
                    slug=unique_slug(Project, title),
                    category=category,
                    short_description=desc,
                    full_description=f"{desc} The final result combines utility, comfort, and a clean premium look.",
                    location=location,
                    is_featured=True,
                )
            )

    if Testimonial.query.count() == 0:
        db.session.add_all(
            [
                Testimonial(
                    client_name="Aarav Mehta",
                    review="The team handled our home interiors with care and clarity. The final execution felt polished and practical.",
                    rating=5,
                    is_featured=True,
                ),
                Testimonial(
                    client_name="Riya Sharma",
                    review="Rockwood Studio made the renovation process easy to understand. Communication was smooth from start to finish.",
                    rating=5,
                    is_featured=True,
                ),
            ]
        )

    db.session.commit()
